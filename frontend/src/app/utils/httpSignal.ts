import { effect, Signal, signal } from "@angular/core";
import { catchError, Observable, of, retry, Subscription, timeout } from "rxjs";

/**
 * Given a function that returns an observable, convert it into a signal. 
 * If the function that is given uses signals, then this will automatically recompute 
 * when the input signal changes.
 * 
 * @param computation 
 * @returns the signal
 */
export function httpSignal<T>(computation: () => Observable<T>): Signal<T | null> & { recompute: () => void } {
    const sig = signal<T | null>(null);

    // Save current subscription to be able to unsubscribe 
    let subscription: Subscription;

    // Create an arrow function that contains the signal updating logic
    const recompute = () => {
        sig.set(null);
        // Before making the new subscription, unsub from the previous one
        if (subscription && !subscription.closed) {
            subscription.unsubscribe();
        }
        const observable = computation().pipe(
            timeout(3000),
            retry(4),
            catchError(() => of(null)) // if error 4 times, return null
        );
        subscription = observable.subscribe((result) => sig.set(result));
    };

    effect(recompute, { allowSignalWrites: true });

    // Add the recompute function to the returned signal, so that it can be called from the outside
    return Object.assign(sig, { recompute });
}