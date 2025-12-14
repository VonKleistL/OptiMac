//
//  StatusBarController.swift
//  OptiMac
//
//  Creates the NSStatusItem with a Phoenix icon and quick actions.
//

import AppKit
import SwiftUI

final class StatusBarController {
    private let statusItem: NSStatusItem
    private let menu = NSMenu()
    private weak var systemMonitor: SystemMonitor?
    private let openMainApp: () -> Void

    init(systemMonitor: SystemMonitor, openMainApp: @escaping () -> Void) {
        self.systemMonitor = systemMonitor
        self.openMainApp = openMainApp

        // Use a fixed length so the item doesn't collapse if the image fails to load
        self.statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)

        configureButtonImage()

        constructMenu()
        statusItem.menu = menu
    }

    private func configureButtonImage() {
        guard let button = statusItem.button else { return }

        if let img = NSImage(named: "MenubarPhoenix") {
            // Full-color asset
            img.isTemplate = false
            button.image = img
            button.imageScaling = .scaleProportionallyDown
            button.appearsDisabled = false
        } else {
            // Fallback: programmatic template icon so it's never invisible
            #if DEBUG
            print("Warning: MenubarPhoenix asset not found. Falling back to template icon.")
            #endif
            let fallback = Self.phoenixIcon(isTemplate: true)
            button.image = fallback
            button.imageScaling = .scaleProportionallyDown
            button.appearsDisabled = false
        }
    }

    private func constructMenu() {
        menu.items.removeAll()

        // Five quick actions
        menu.addItem(withTitle: "Purge Inactive Memory", action: #selector(purgeMemory), keyEquivalent: "")
        menu.addItem(withTitle: "Flush DNS Cache", action: #selector(flushDNS), keyEquivalent: "")
        menu.addItem(withTitle: "Clear System Caches", action: #selector(clearCaches), keyEquivalent: "")
        menu.addItem(withTitle: "Clean Homebrew", action: #selector(cleanHomebrew), keyEquivalent: "")
        menu.addItem(withTitle: "Rebuild Spotlight Index", action: #selector(rebuildSpotlight), keyEquivalent: "")

        menu.addItem(NSMenuItem.separator())

        // Open main app
        let openItem = NSMenuItem(title: "Open OptiMac", action: #selector(openApp), keyEquivalent: "")
        menu.addItem(openItem)

        // Quit
        let quitItem = NSMenuItem(title: "Quit", action: #selector(quitApp), keyEquivalent: "q")
        menu.addItem(quitItem)

        // Target
        for item in menu.items {
            item.target = self
        }
    }

    // MARK: - Actions (wired to SystemMonitor quick task ids)
    @objc private func purgeMemory() { runTasks(ids: ["purge_memory"]) }
    @objc private func flushDNS() { runTasks(ids: ["flush_dns"]) }
    @objc private func clearCaches() { runTasks(ids: ["clear_caches"]) }
    @objc private func cleanHomebrew() { runTasks(ids: ["optimize_homebrew"]) }
    @objc private func rebuildSpotlight() { runTasks(ids: ["reindex_spotlight"]) }

    @objc private func openApp() {
        openMainApp()
    }

    @objc private func quitApp() {
        NSApp.terminate(nil)
    }

    private func runTasks(ids: [String]) {
        guard let monitor = systemMonitor else { return }
        monitor.selectedTasks = Set(ids)
        monitor.runOptimization()
    }

    // MARK: - Phoenix Icon (template fallback)
    static func phoenixIcon(isTemplate: Bool) -> NSImage {
        let size = NSSize(width: 18, height: 18)
        let image = NSImage(size: size)
        image.lockFocus()

        let bounds = NSRect(origin: .zero, size: size)
        let center = CGPoint(x: bounds.midX, y: bounds.midY)

        let primary = NSColor.white
        let secondary = NSColor.white.withAlphaComponent(0.9)

        let body = NSBezierPath()
        body.move(to: CGPoint(x: center.x, y: 2))
        body.curve(to: CGPoint(x: 2, y: center.y),
                   controlPoint1: CGPoint(x: center.x - 5, y: 2),
                   controlPoint2: CGPoint(x: 2, y: center.y - 4))
        body.curve(to: CGPoint(x: center.x, y: size.height - 2),
                   controlPoint1: CGPoint(x: 2, y: center.y + 6),
                   controlPoint2: CGPoint(x: center.x - 3, y: size.height - 2))
        body.curve(to: CGPoint(x: size.width - 2, y: center.y),
                   controlPoint1: CGPoint(x: center.x + 3, y: size.height - 2),
                   controlPoint2: CGPoint(x: size.width - 2, y: center.y + 6))
        body.curve(to: CGPoint(x: center.x, y: 2),
                   controlPoint1: CGPoint(x: size.width - 2, y: center.y - 4),
                   controlPoint2: CGPoint(x: center.x + 5, y: 2))
        primary.setFill()
        body.fill()

        let leftWing = NSBezierPath()
        leftWing.move(to: CGPoint(x: center.x - 2, y: center.y + 2))
        leftWing.curve(to: CGPoint(x: 1, y: center.y + 1),
                       controlPoint1: CGPoint(x: center.x - 7, y: center.y + 6),
                       controlPoint2: CGPoint(x: 2, y: center.y + 4))
        leftWing.curve(to: CGPoint(x: center.x - 1, y: center.y - 1),
                       controlPoint1: CGPoint(x: 0, y: center.y),
                       controlPoint2: CGPoint(x: center.x - 4, y: center.y - 2))
        secondary.setFill()
        leftWing.fill()

        let rightWing = NSBezierPath()
        rightWing.move(to: CGPoint(x: center.x + 2, y: center.y + 2))
        rightWing.curve(to: CGPoint(x: size.width - 1, y: center.y + 1),
                        controlPoint1: CGPoint(x: center.x + 7, y: center.y + 6),
                        controlPoint2: CGPoint(x: size.width - 2, y: center.y + 4))
        rightWing.curve(to: CGPoint(x: center.x + 1, y: center.y - 1),
                        controlPoint1: CGPoint(x: size.width, y: center.y),
                        controlPoint2: CGPoint(x: center.x + 4, y: center.y - 2))
        secondary.setFill()
        rightWing.fill()

        image.unlockFocus()
        image.isTemplate = isTemplate
        return image
    }
}
