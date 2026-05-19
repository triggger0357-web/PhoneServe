import type { SessionAuthObject } from '@clerk/backend';
import type { GetAuthFnNoRequest, RedirectFun } from '@clerk/backend/internal';
import { redirect } from 'next/navigation';
import type { AuthProtect } from '../../server/protect';
/**
 * `Auth` object of the currently active user and the `redirectToSignIn()` method.
 */
export type SessionAuthWithRedirect = SessionAuthObject & {
    /**
     * The `auth()` helper returns the `redirectToSignIn()` method, which you can use to redirect the user to the sign-in page.
     *
     * @param [returnBackUrl] {string | URL} - The URL to redirect the user back to after they sign in.
     *
     * > [!NOTE]
     * > `auth()` on the server-side can only access redirect URLs defined via [environment variables](https://clerk.com/docs/guides/development/clerk-environment-variables#sign-in-and-sign-up-redirects) or [`clerkMiddleware` dynamic keys](https://clerk.com/docs/reference/nextjs/clerk-middleware#dynamic-keys).
     */
    redirectToSignIn: RedirectFun<ReturnType<typeof redirect>>;
    /**
     * The `auth()` helper returns the `redirectToSignUp()` method, which you can use to redirect the user to the sign-up page.
     *
     * @param [returnBackUrl] {string | URL} - The URL to redirect the user back to after they sign up.
     *
     * > [!NOTE]
     * > `auth()` on the server-side can only access redirect URLs defined via [environment variables](https://clerk.com/docs/guides/development/clerk-environment-variables#sign-in-and-sign-up-redirects) or [`clerkMiddleware` dynamic keys](https://clerk.com/docs/reference/nextjs/clerk-middleware#dynamic-keys).
     */
    redirectToSignUp: RedirectFun<ReturnType<typeof redirect>>;
};
export type AuthFn = GetAuthFnNoRequest<SessionAuthWithRedirect, true> & {
    /**
     * `auth` includes a single property, the `protect()` method, which you can use in two ways:
     * - to check if a user is authenticated (signed in)
     * - to check if a user is authorized (has the correct roles or permissions) to access something, such as a component or a route handler
     *
     * The following table describes how auth.protect() behaves based on user authentication or authorization status:
     *
     * | Authenticated | Authorized | `auth.protect()` will |
     * | - | - | - |
     * | Yes | Yes | Return the [`Auth`](https://clerk.com/docs/reference/backend/types/auth-object) object. |
     * | Yes | No | Return a `404` error. |
     * | No | No | Redirect the user to the sign-in page\*. |
     *
     * > [!IMPORTANT]
     * > \*For non-document requests, such as API requests, `auth.protect()` returns a `404` error to users who aren't authenticated.
     *
     * `auth.protect()` can be used to check if a user is authenticated or authorized to access certain parts of your application or even entire routes. See detailed examples in the [dedicated guide](https://clerk.com/docs/organizations/verify-user-permissions).
     */
    protect: AuthProtect;
};
/**
 * The `auth()` helper returns the [`Auth`](https://clerk.com/docs/reference/backend/types/auth-object) object of the currently active user, as well as the [`redirectToSignIn()`](https://clerk.com/docs/reference/nextjs/app-router/auth#redirect-to-sign-in) method.
 *
 * - Only available for App Router.
 * - Only works on the server-side, such as in Server Components, Route Handlers, and Server Actions.
 * - Requires [`clerkMiddleware()`](https://clerk.com/docs/reference/nextjs/clerk-middleware) to be configured.
 */
export declare const auth: AuthFn;
//# sourceMappingURL=auth.d.ts.map