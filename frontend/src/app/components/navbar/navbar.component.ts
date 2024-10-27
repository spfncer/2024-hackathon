import { CommonModule, DOCUMENT } from "@angular/common";
import { Component, computed, effect, Inject, Signal } from "@angular/core";
import { updatePrimaryPalette } from 'primeng/themes';

import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from "primeng/avatar";
import { BadgeModule } from "primeng/badge";
import { OverlayBadgeModule } from 'primeng/overlaybadge';
import { ButtonModule } from "primeng/button";
import { DividerModule } from 'primeng/divider';
import { DrawerModule } from 'primeng/drawer';
import { InternetConnectionService } from "../../services/internet-connection/internet-connection.service";

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [
        CommonModule,
        MenubarModule,
        AvatarModule,
        BadgeModule,
        OverlayBadgeModule,
        ButtonModule,
        DividerModule,
        DrawerModule
    ],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent {
    private root: HTMLHtmlElement;
    public isDarkMode: boolean = false;

    public colorMenuVisible: boolean = false;
    public primaryColors = [
        { name: "emerald", value: 'rgb(16, 185, 129)' },
        { name: "green", value: 'rgb(34, 197, 94)' },
        { name: "lime", value: 'rgb(132, 204 ,22)' },
        { name: "red", value: 'rgb(249, 115, 22)' },
        { name: "orange", value: 'rgb(245, 158, 11)' },
        { name: "amber", value: 'rgb(234, 179, 8)' },
        { name: "yellow", value: 'rgb(20, 184, 166)' },
        { name: "teal", value: 'rgb(16, 185, 129)' },
        { name: "cyan", value: 'rgb(6, 182, 212)' },
        { name: "sky", value: 'rgb(14, 165, 233)' },
        { name: "blue", value: 'rgb(59, 130, 246)' },
        { name: "indigo", value: 'rgb(99, 102, 241)' },
        { name: "violet", value: 'rgb(139, 92, 246)' },
        { name: "purple", value: 'rgb(168, 85, 247)' },
        { name: "fuchsia", value: 'rgb(217, 70, 239)' },
        { name: "pink", value: 'rgb(236, 72, 153)' },
        { name: "rose", value: 'rgb(244, 63, 94)' },
        { name: "slate", value: 'rgb(100, 116, 139)' },
        { name: "gray", value: 'rgb(107, 114, 128)' },
        { name: "zinc", value: 'rgb(113, 113, 122)' },
        { name: "neutral", value: 'rgb(115, 115, 115)' },
        { name: "stone", value: 'rgb(120, 113, 108)' }
    ];

    constructor(public internetConnection: InternetConnectionService, @Inject(DOCUMENT) private document: Document) {
        this.root = this.document.querySelector('html')!;
    }

    changePrimaryColor(colorName: string) {
        updatePrimaryPalette({
            50: `{${colorName}.50}`,
            100: `{${colorName}.100}`,
            200: `{${colorName}.200}`,
            300: `{${colorName}.300}`,
            400: `{${colorName}.400}`,
            500: `{${colorName}.500}`,
            600: `{${colorName}.600}`,
            700: `{${colorName}.700}`,
            800: `{${colorName}.800}`,
            900: `{${colorName}.900}`,
            950: `{${colorName}.950}`
        });
    }

    toggleDarkMode() {
        this.isDarkMode = this.root.classList.toggle('dark-mode');
    }
}
