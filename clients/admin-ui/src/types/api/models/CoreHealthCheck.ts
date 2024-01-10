/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Server Healthcheck schema
 */
export type CoreHealthCheck = {
  webserver: string;
  version: string;
  cache: CoreHealthCheck.cache;
  invite_users_via_email: boolean;
};

export namespace CoreHealthCheck {
  export enum cache {
    HEALTHY = "healthy",
    UNHEALTHY = "unhealthy",
    NO_CACHE_CONFIGURED = "no cache configured",
  }
}
