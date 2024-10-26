import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";

import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from "primeng/avatar";
import { BadgeModule } from "primeng/badge";
import { MenuItem } from "primeng/api";

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
    styleUrl: 'navbar.component.css'
})
export class NavbarComponent { }