/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/node-sync',
        destination: '/api/handshake',
      },
    ];
  },
};
module.exports = nextConfig;
