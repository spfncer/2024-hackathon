import { Injectable, signal } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class WindowService {
    get nativeWindow(): Window { return window; };
}

/**
 * A service which allows components to view internet connection status according to the browser. 
 * This service wraps the Window online event (https://developer.mozilla.org/en-US/docs/Web/API/Window/online_event).
 * 
 * Firewalls may mess up some of this functionality.
 */
@Injectable({
    providedIn: 'root'
})
export class InternetConnectionService {
    /**
     * Private signal used to montior / update internet connection status based on browser events.
     */
    private isOnlineSignal = signal<boolean>(true);

    /**
     * Public readonly signal which is used to monitor internet connection status.
     */
    public readonly isOnline = this.isOnlineSignal.asReadonly();

    /**
     * Initializes the event listeners for the service.
     */
    constructor(private windowService: WindowService) {
        this.windowService.nativeWindow.addEventListener('online', () => this.isOnlineSignal.set(true));
        this.windowService.nativeWindow.addEventListener('offline', () => this.isOnlineSignal.set(false));
    }
}