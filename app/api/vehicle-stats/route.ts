import { NextApiRequest } from 'next';
import pool from '@/lib/db';
import { NextResponse } from 'next/server';

export async function GET(req: NextApiRequest) {
    if (req.method === 'GET') {
        try {
            const query = `
                SELECT *
                    FROM counts
                ORDER BY timestamp DESC
            `;
            const [result] = await pool.execute(query);

            if (!result) {
                NextResponse.json({ data: [] }, { status: 200 });
            }

            return NextResponse.json({ data: result }, { status: 200 });
        } catch (error) {
            console.error('Error getting counts:', error);
            NextResponse.json({ error: 'Internal server error' });
        }
    } else {
        NextResponse.json({ message: 'Method not allowed' });
    }
}
