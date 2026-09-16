#!/usr/bin/env swift

import AppKit
import AVFoundation
import Foundation
import ImageIO

private let usage = """
Usage:
  sample_media.swift MEDIA_ROOT OUTPUT_DIR [--item NAME ...] [--items-file FILE] [--deep] [--max-edge PIXELS]

MEDIA_ROOT contains one directory per post. A post directory may contain video.mp4
(cover.jpg is ignored) or image_01.jpg, image_02.jpg, and so on.

Defaults:
  video <= 60 seconds: 5 evenly spaced frames
  video > 60 seconds:  7 evenly spaced frames
  --deep:               9 frames for every video

OUTPUT_DIR is never overwritten. If it already exists, a numeric suffix is used.
Per-item failures are recorded in manifest.json; they do not stop the batch.
--items-file accepts one directory name per line or links.tsv from init_fast_batch.py.
"""

private struct Options {
    let mediaRoot: URL
    let requestedOutputRoot: URL
    let items: [String]
    let deep: Bool
    let maxEdge: Int
}

private enum CLIError: LocalizedError {
    case message(String)

    var errorDescription: String? {
        switch self {
        case .message(let text): return text
        }
    }
}

private struct SheetCell {
    let image: CGImage
    let label: String
}

private func stderr(_ text: String) {
    FileHandle.standardError.write(Data((text + "\n").utf8))
}

private func itemNames(from file: String) throws -> [String] {
    let text = try String(contentsOfFile: file, encoding: .utf8)
    let lines = text.split(whereSeparator: \Character.isNewline).map(String.init)
    guard let first = lines.first else { return [] }
    let header = first.split(separator: "\t", omittingEmptySubsequences: false).map(String.init)
    if let column = header.firstIndex(of: "media_item") {
        return lines.dropFirst().compactMap { line in
            let fields = line.split(separator: "\t", omittingEmptySubsequences: false).map(String.init)
            return column < fields.count && !fields[column].isEmpty ? fields[column] : nil
        }
    }
    return lines.map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty }
}

private func parseArguments() throws -> Options? {
    let arguments = Array(CommandLine.arguments.dropFirst())
    if arguments.contains("--help") || arguments.contains("-h") {
        print(usage)
        return nil
    }

    var positional: [String] = []
    var requestedItems: [String] = []
    var deep = false
    var maxEdge = 1024
    var index = 0

    while index < arguments.count {
        let argument = arguments[index]
        switch argument {
        case "--deep":
            deep = true
        case "--item":
            index += 1
            guard index < arguments.count else {
                throw CLIError.message("--item requires a directory name")
            }
            requestedItems.append(arguments[index])
        case "--items-file":
            index += 1
            guard index < arguments.count else {
                throw CLIError.message("--items-file requires a file path")
            }
            requestedItems.append(contentsOf: try itemNames(from: arguments[index]))
        case "--max-edge":
            index += 1
            guard index < arguments.count, let value = Int(arguments[index]), (320...4096).contains(value) else {
                throw CLIError.message("--max-edge requires an integer from 320 to 4096")
            }
            maxEdge = value
        default:
            if argument.hasPrefix("-") {
                throw CLIError.message("unknown option: \(argument)")
            }
            positional.append(argument)
        }
        index += 1
    }

    guard positional.count == 2 else {
        throw CLIError.message("expected MEDIA_ROOT and OUTPUT_DIR\n\n\(usage)")
    }

    var seen = Set<String>()
    let items = requestedItems.filter { seen.insert($0).inserted }
    return Options(
        mediaRoot: URL(fileURLWithPath: positional[0]).standardizedFileURL,
        requestedOutputRoot: URL(fileURLWithPath: positional[1]).standardizedFileURL,
        items: items,
        deep: deep,
        maxEdge: maxEdge
    )
}

private func reserveOutputRoot(_ requested: URL) throws -> URL {
    let fileManager = FileManager.default
    let parent = requested.deletingLastPathComponent()
    let baseName = requested.lastPathComponent
    try fileManager.createDirectory(at: parent, withIntermediateDirectories: true)

    for suffix in 1...10_000 {
        let name = suffix == 1 ? baseName : "\(baseName)-\(suffix)"
        let candidate = parent.appendingPathComponent(name, isDirectory: true)
        if !fileManager.fileExists(atPath: candidate.path) {
            try fileManager.createDirectory(at: candidate, withIntermediateDirectories: false)
            return candidate
        }
    }
    throw CLIError.message("could not reserve a unique output directory near \(requested.path)")
}

private func isDirectory(_ url: URL) -> Bool {
    var value: ObjCBool = false
    return FileManager.default.fileExists(atPath: url.path, isDirectory: &value) && value.boolValue
}

private func validItemName(_ name: String) -> Bool {
    !name.isEmpty && name != "." && name != ".." && !name.contains("/") && !name.contains("\\")
}

private func discoverItems(_ options: Options) throws -> [(name: String, url: URL?)] {
    guard isDirectory(options.mediaRoot) else {
        throw CLIError.message("MEDIA_ROOT is not a directory: \(options.mediaRoot.path)")
    }

    if !options.items.isEmpty {
        return options.items.map { name in
            guard validItemName(name) else { return (name, nil) }
            let url = options.mediaRoot.appendingPathComponent(name, isDirectory: true)
            return (name, isDirectory(url) ? url : nil)
        }
    }

    return try FileManager.default.contentsOfDirectory(
        at: options.mediaRoot,
        includingPropertiesForKeys: [.isDirectoryKey],
        options: [.skipsHiddenFiles]
    )
    .filter(isDirectory)
    .map { ($0.lastPathComponent, $0) }
    .sorted { $0.0.localizedStandardCompare($1.0) == .orderedAscending }
}

private func rounded(_ value: Double, places: Int = 3) -> Double {
    let factor = pow(10.0, Double(places))
    return (value * factor).rounded() / factor
}

private func jpegData(for image: CGImage, quality: CGFloat) throws -> Data {
    let bitmap = NSBitmapImageRep(cgImage: image)
    guard let data = bitmap.representation(using: .jpeg, properties: [.compressionFactor: quality]) else {
        throw CLIError.message("JPEG encoding failed")
    }
    return data
}

private func writeJPEG(_ image: CGImage, to url: URL, quality: CGFloat = 0.9) throws {
    try jpegData(for: image, quality: quality).write(to: url, options: .atomic)
}

private func thumbnail(at url: URL, maxEdge: Int) throws -> CGImage {
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil) else {
        throw CLIError.message("cannot open image \(url.lastPathComponent)")
    }
    let options: [CFString: Any] = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxEdge,
        kCGImageSourceShouldCacheImmediately: true,
    ]
    guard let image = CGImageSourceCreateThumbnailAtIndex(source, 0, options as CFDictionary) else {
        throw CLIError.message("cannot decode image \(url.lastPathComponent)")
    }
    return image
}

private func aspectFit(_ image: CGImage, inside box: NSRect) -> NSRect {
    let width = CGFloat(image.width)
    let height = CGFloat(image.height)
    let scale = min(box.width / width, box.height / height)
    let fittedWidth = width * scale
    let fittedHeight = height * scale
    return NSRect(
        x: box.minX + (box.width - fittedWidth) / 2,
        y: box.minY + (box.height - fittedHeight) / 2,
        width: fittedWidth,
        height: fittedHeight
    )
}

private func makeContactSheet(cells: [SheetCell], header: String, target: URL) throws {
    guard !cells.isEmpty else { throw CLIError.message("no images for contact sheet") }

    let columns = 3
    let tileWidth = 420
    let tileHeight = 420
    let labelHeight = 34
    let headerHeight = 58
    let rowCount = Int(ceil(Double(cells.count) / Double(columns)))
    let canvasWidth = columns * tileWidth
    let canvasHeight = headerHeight + rowCount * (tileHeight + labelHeight)

    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: canvasWidth,
        pixelsHigh: canvasHeight,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ), let context = NSGraphicsContext(bitmapImageRep: bitmap) else {
        throw CLIError.message("cannot allocate contact-sheet canvas")
    }

    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    NSColor(calibratedWhite: 0.075, alpha: 1).setFill()
    NSBezierPath.fill(NSRect(x: 0, y: 0, width: canvasWidth, height: canvasHeight))

    let headerAttributes: [NSAttributedString.Key: Any] = [
        .font: NSFont.monospacedSystemFont(ofSize: 21, weight: .semibold),
        .foregroundColor: NSColor.white,
    ]
    let labelAttributes: [NSAttributedString.Key: Any] = [
        .font: NSFont.monospacedSystemFont(ofSize: 16, weight: .medium),
        .foregroundColor: NSColor(calibratedWhite: 0.94, alpha: 1),
    ]
    (header as NSString).draw(
        in: NSRect(x: 18, y: canvasHeight - headerHeight + 15, width: canvasWidth - 36, height: 30),
        withAttributes: headerAttributes
    )

    for (index, cell) in cells.enumerated() {
        let row = index / columns
        let column = index % columns
        let cellTop = CGFloat(canvasHeight - headerHeight - row * (tileHeight + labelHeight))
        let tile = NSRect(
            x: CGFloat(column * tileWidth + 4),
            y: cellTop - CGFloat(tileHeight) + 4,
            width: CGFloat(tileWidth - 8),
            height: CGFloat(tileHeight - 8)
        )
        NSColor(calibratedWhite: 0.02, alpha: 1).setFill()
        NSBezierPath.fill(tile)

        let destination = aspectFit(cell.image, inside: tile)
        let drawable = NSImage(
            cgImage: cell.image,
            size: NSSize(width: cell.image.width, height: cell.image.height)
        )
        drawable.draw(
            in: destination,
            from: .zero,
            operation: .copy,
            fraction: 1,
            respectFlipped: false,
            hints: [.interpolation: NSImageInterpolation.high]
        )
        (cell.label as NSString).draw(
            in: NSRect(
                x: CGFloat(column * tileWidth + 14),
                y: cellTop - CGFloat(tileHeight + labelHeight) + 7,
                width: CGFloat(tileWidth - 28),
                height: CGFloat(labelHeight - 8)
            ),
            withAttributes: labelAttributes
        )
    }

    context.flushGraphics()
    NSGraphicsContext.restoreGraphicsState()
    guard let data = bitmap.representation(using: .jpeg, properties: [.compressionFactor: 0.9]) else {
        throw CLIError.message("contact-sheet JPEG encoding failed")
    }
    try data.write(to: target, options: .atomic)
}

private func relativePath(_ url: URL, from root: URL) -> String {
    let rootPath = root.standardizedFileURL.path
    let path = url.standardizedFileURL.path
    let prefix = rootPath.hasSuffix("/") ? rootPath : rootPath + "/"
    return path.hasPrefix(prefix) ? String(path.dropFirst(prefix.count)) : path
}

private func imageFiles(in item: URL) throws -> [URL] {
    let supported = Set(["jpg", "jpeg", "png", "heic", "heif", "webp", "tif", "tiff"])
    return try FileManager.default.contentsOfDirectory(
        at: item,
        includingPropertiesForKeys: [.isRegularFileKey],
        options: [.skipsHiddenFiles]
    )
    .filter {
        $0.deletingPathExtension().lastPathComponent.lowercased().hasPrefix("image_") &&
            supported.contains($0.pathExtension.lowercased())
    }
    .sorted { $0.lastPathComponent.localizedStandardCompare($1.lastPathComponent) == .orderedAscending }
}

private func videoFile(in item: URL) throws -> URL? {
    let exact = item.appendingPathComponent("video.mp4")
    if FileManager.default.fileExists(atPath: exact.path) { return exact }

    let supported = Set(["mp4", "mov", "m4v"])
    return try FileManager.default.contentsOfDirectory(
        at: item,
        includingPropertiesForKeys: [.isRegularFileKey],
        options: [.skipsHiddenFiles]
    )
    .filter {
        $0.deletingPathExtension().lastPathComponent.lowercased() == "video" &&
            supported.contains($0.pathExtension.lowercased())
    }
    .sorted { $0.lastPathComponent < $1.lastPathComponent }
    .first
}

private func processVideo(
    itemName: String,
    itemURL: URL,
    videoURL: URL,
    outputRoot: URL,
    deep: Bool,
    maxEdge: Int
) async throws -> [String: Any] {
    let asset = AVURLAsset(url: videoURL)
    let duration = CMTimeGetSeconds(try await asset.load(.duration))
    guard duration.isFinite, duration > 0 else { throw CLIError.message("invalid video duration") }
    guard let track = try await asset.loadTracks(withMediaType: .video).first else {
        throw CLIError.message("no video track")
    }

    let naturalSize = try await track.load(.naturalSize)
    let preferredTransform = try await track.load(.preferredTransform)
    let transformed = naturalSize.applying(preferredTransform)
    let width = Int(abs(transformed.width).rounded())
    let height = Int(abs(transformed.height).rounded())
    let frameCount = deep ? 9 : (duration > 60 ? 7 : 5)
    let itemOutput = outputRoot
        .appendingPathComponent("items", isDirectory: true)
        .appendingPathComponent(itemName, isDirectory: true)
    try FileManager.default.createDirectory(at: itemOutput, withIntermediateDirectories: true)

    let generator = AVAssetImageGenerator(asset: asset)
    generator.appliesPreferredTrackTransform = true
    generator.maximumSize = CGSize(width: maxEdge, height: maxEdge)
    generator.requestedTimeToleranceBefore = CMTime(seconds: 0.2, preferredTimescale: 600)
    generator.requestedTimeToleranceAfter = CMTime(seconds: 0.2, preferredTimescale: 600)

    var cells: [SheetCell] = []
    var sampleSeconds: [Double] = []
    var framePaths: [String] = []
    let edgeMargin = min(0.05, duration / 4)

    for index in 0..<frameCount {
        var requested = duration * (Double(index) + 0.5) / Double(frameCount)
        requested = max(edgeMargin, min(duration - edgeMargin, requested))
        let generated = try await generator.image(
            at: CMTime(seconds: requested, preferredTimescale: 600)
        )
        let image = generated.image
        let actualValue = CMTimeGetSeconds(generated.actualTime)
        let actualSeconds = actualValue.isFinite ? actualValue : requested
        let frameName = String(format: "frame_%02d_%07.2fs.jpg", index + 1, actualSeconds)
        let frameURL = itemOutput.appendingPathComponent(frameName)
        try writeJPEG(image, to: frameURL, quality: 0.9)
        cells.append(SheetCell(image: image, label: String(format: "%02d  %.2fs", index + 1, actualSeconds)))
        sampleSeconds.append(rounded(actualSeconds))
        framePaths.append(relativePath(frameURL, from: outputRoot))
    }

    let sheetURL = itemOutput.appendingPathComponent("contact_sheet.jpg")
    let header = String(format: "%@  VIDEO  %.2fs  %dx%d  %d frames", itemName, duration, width, height, frameCount)
    try makeContactSheet(cells: cells, header: header, target: sheetURL)

    let sourceRelative = relativePath(videoURL, from: itemURL.deletingLastPathComponent())
    return [
        "item": itemName,
        "status": "ok",
        "type": "video",
        "source": sourceRelative,
        "duration_seconds": rounded(duration),
        "dimensions": "\(width)x\(height)",
        "frame_count": frameCount,
        "sample_seconds": sampleSeconds,
        "frames": framePaths,
        "contact_sheet": relativePath(sheetURL, from: outputRoot),
    ]
}

private func processImages(
    itemName: String,
    itemURL: URL,
    images: [URL],
    outputRoot: URL,
    maxEdge: Int
) throws -> [String: Any] {
    let itemOutput = outputRoot
        .appendingPathComponent("items", isDirectory: true)
        .appendingPathComponent(itemName, isDirectory: true)
    try FileManager.default.createDirectory(at: itemOutput, withIntermediateDirectories: true)

    var cells: [SheetCell] = []
    for (index, source) in images.enumerated() {
        let image = try thumbnail(at: source, maxEdge: maxEdge)
        cells.append(SheetCell(image: image, label: String(format: "%02d  %@", index + 1, source.lastPathComponent)))
    }

    let sheetURL = itemOutput.appendingPathComponent("contact_sheet.jpg")
    try makeContactSheet(
        cells: cells,
        header: "\(itemName)  IMAGE NOTE  \(images.count) images",
        target: sheetURL
    )

    return [
        "item": itemName,
        "status": "ok",
        "type": "image",
        "image_count": images.count,
        "sources": images.map { relativePath($0, from: itemURL.deletingLastPathComponent()) },
        "contact_sheet": relativePath(sheetURL, from: outputRoot),
    ]
}

private func processItem(
    name: String,
    url: URL,
    options: Options,
    outputRoot: URL
) async throws -> [String: Any] {
    if let video = try videoFile(in: url) {
        return try await processVideo(
            itemName: name,
            itemURL: url,
            videoURL: video,
            outputRoot: outputRoot,
            deep: options.deep,
            maxEdge: options.maxEdge
        )
    }

    let images = try imageFiles(in: url)
    guard !images.isEmpty else { throw CLIError.message("no video.mp4 or image_* media") }
    return try processImages(
        itemName: name,
        itemURL: url,
        images: images,
        outputRoot: outputRoot,
        maxEdge: options.maxEdge
    )
}

private func writeJSON(_ value: Any, to url: URL) throws {
    let data = try JSONSerialization.data(withJSONObject: value, options: [.sortedKeys])
    try data.write(to: url, options: .atomic)
}

do {
    guard let options = try parseArguments() else { exit(0) }
    let started = ProcessInfo.processInfo.systemUptime
    let discovered = try discoverItems(options)
    let outputRoot = try reserveOutputRoot(options.requestedOutputRoot)

    var rows: [[String: Any]] = []
    for item in discovered {
        guard let itemURL = item.url else {
            rows.append(["item": item.name, "status": "error", "error": "item directory not found or invalid"])
            continue
        }
        do {
            rows.append(try await processItem(name: item.name, url: itemURL, options: options, outputRoot: outputRoot))
        } catch {
            rows.append(["item": item.name, "status": "error", "error": error.localizedDescription])
        }
    }

    let okCount = rows.filter { ($0["status"] as? String) == "ok" }.count
    let failedCount = rows.count - okCount
    let videoCount = rows.filter { ($0["status"] as? String) == "ok" && ($0["type"] as? String) == "video" }.count
    let imageCount = rows.filter { ($0["status"] as? String) == "ok" && ($0["type"] as? String) == "image" }.count
    let elapsed = rounded(ProcessInfo.processInfo.systemUptime - started)
    let manifestURL = outputRoot.appendingPathComponent("manifest.json")
    let manifest: [String: Any] = [
        "schema_version": 1,
        "mode": options.deep ? "deep-9" : "auto-5-or-7",
        "media_root": options.mediaRoot.path,
        "output_root": outputRoot.path,
        "elapsed_seconds": elapsed,
        "counts": [
            "items": rows.count,
            "ok": okCount,
            "failed": failedCount,
            "video": videoCount,
            "image": imageCount,
        ],
        "items": rows,
    ]
    try writeJSON(manifest, to: manifestURL)

    let summary: [String: Any] = [
        "output_root": outputRoot.path,
        "manifest": manifestURL.path,
        "elapsed_seconds": elapsed,
        "ok": okCount,
        "failed": failedCount,
    ]
    let summaryData = try JSONSerialization.data(withJSONObject: summary, options: [.sortedKeys])
    print(String(decoding: summaryData, as: UTF8.self))
    exit(rows.isEmpty || okCount == 0 ? 1 : 0)
} catch {
    stderr("sample_media: \(error.localizedDescription)")
    exit(2)
}
