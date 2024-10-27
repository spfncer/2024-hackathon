import { CommonModule, DOCUMENT } from "@angular/common";
import { Component, computed, effect, Inject, Signal } from "@angular/core";

import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from "primeng/avatar";
import { BadgeModule } from "primeng/badge";
import { OverlayBadgeModule } from 'primeng/overlaybadge';
import { ButtonModule } from "primeng/button";
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
        ButtonModule
    ],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent {
    private root: HTMLHtmlElement;
    public isDarkMode: boolean = false;

    constructor(public internetConnection: InternetConnectionService, @Inject(DOCUMENT) private document: Document) {
        this.root = this.document.querySelector('html')!;
    }

    toggleDarkMode() {
        this.isDarkMode = this.root.classList.toggle('dark-mode');
    }
}