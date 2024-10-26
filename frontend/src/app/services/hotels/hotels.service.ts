import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: "root"
})
export class HotelsService {

    static readonly REST_API_SERVER = "http://localhost:8000/";

    constructor(private httpClient: HttpClient) { }

    // getter 

}