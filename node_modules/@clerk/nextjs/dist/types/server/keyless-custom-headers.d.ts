interface MetadataHeaders {
    nodeVersion?: string;
    nextVersion?: string;
    npmConfigUserAgent?: string;
    userAgent: string;
    port?: string;
    host: string;
    xHost: string;
    xPort: string;
    xProtocol: string;
    xClerkAuthStatus: string;
    isCI: boolean;
}
/**
 * Collects metadata from the environment and request headers
 */
export declare function collectKeylessMetadata(): Promise<MetadataHeaders>;
/**
 * Converts metadata to HTTP headers
 */
export declare function formatMetadataHeaders(metadata: MetadataHeaders): Promise<Headers>;
export {};
//# sourceMappingURL=keyless-custom-headers.d.ts.map