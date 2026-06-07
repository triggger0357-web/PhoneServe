if (typeof window === 'undefined') {
  global.window = {} as any;
  global.localStorage = {
    getItem: () => null,
    setItem: () => null,
    removeItem: () => null,
    clear: () => null,
    length: 0,
    key: () => null,
  } as any;
}

const nextConfig = {
  devIndicators: {
    appIsrStatus: false,
  },
  experimental: {
    allowedDevOrigins: ["localhost:3000", "127.0.0.1:8080"]
  }
};

export default nextConfig;
