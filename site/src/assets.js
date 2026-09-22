/** Static deployment uses local paths. The optional single-file artifact supplies data URLs. */
export const assetUrl=path=>window.__BINGBONG_ASSETS?.[path]??path;
