/**
 * Next.js configuration
 */

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost/api/v1',
  },
  
  // Image configuration
  images: {
    domains: ['localhost'],
    unoptimized: true,
  },
  
  /*
  // Experimental features
  experimental: {
    // Enable server actions
    serverActions: {
      bodySizeLimit: '10mb',
    },
  },
  
  // Production optimizations
  poweredByHeader: false,
  compress: true,
  
  // Webpack configuration
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
    };
    return config;
  },
  */
};


export default nextConfig;
