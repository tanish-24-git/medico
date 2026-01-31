/**
 * Health check API route for Next.js
 */
export async function GET() {
  return Response.json({ status: 'healthy' });
}
