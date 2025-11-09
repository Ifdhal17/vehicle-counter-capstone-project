import pool from '@/lib/db';
import { NextResponse, NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
    if (req.method === 'POST') {
        const body = await req.json();

        const timestamp = new Date();

        const { location, car_count, motorbike_count, truck_count, bus_count } = body;

        try {
            const query = `
                INSERT INTO counts (timestamp, location, car_count, motorbike_count, truck_count, bus_count)
                VALUES (?, ?, ?, ?, ?, ?);`;
            const values = [timestamp, location, car_count, motorbike_count, truck_count, bus_count];

            await pool.execute(query, values);

            return NextResponse.json({ message: 'Counts updated successfully', body }, { status: 201 });
        } catch (error) {
            console.error('Error updating counts:', error);
            return NextResponse.json({ error: 'Internal server error', message: error }, { status: 500 });
        }
    } else {
        return NextResponse.json({ message: 'Method not allowed' }, { status: 403 });
    }
}
