import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";

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

    constructor(private internetConnection: InternetConnectionService) {
        console.log(this.internetConnection.isOnline());
    }

}