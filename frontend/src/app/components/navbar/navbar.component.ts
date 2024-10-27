import { CommonModule } from "@angular/common";
import { Component, computed, effect, Signal } from "@angular/core";

import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from "primeng/avatar";
import { BadgeModule } from "primeng/badge";
import { InternetConnectionService } from "../../services/internet-connection/internet-connection.service";

@Component({
    selector: 'app-navbar',
    standalone: true,
    imports: [
        CommonModule,
        MenubarModule,
        AvatarModule,
        BadgeModule
    ],
    templateUrl: './navbar.component.html',
    styleUrl: './navbar.component.css'
})
export class NavbarComponent {
    public wifiImagePath: Signal<string>

    constructor(public internetConnection: InternetConnectionService) {
        this.wifiImagePath = computed(() => this.internetConnection.isOnline() ? "wi-fi.png" : "wi-fi-off.png");
    }

}