import { connectToDatabase } from '../../utils/db'; // Example helper function
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        console.log('Request received:', req.body); // Log incoming request
        const { vehicleClass, detectionTime, location } = req.body;

        try {
            console.log('Connecting to database...');
            const db = await connectToDatabase();
            console.log('Connected successfully.');

            console.log('Inserting data:', { vehicleClass, detectionTime, location });
            const result = await db.collection('vehicles').insertOne({
                vehicleClass,
                detectionTime,
                location,
            });

            console.log('Insert successful:', result);
            res.status(200).json({ message: 'Vehicle inserted successfully', result });
        } catch (error) {
            console.error('Error inserting vehicle:', error); // Log error details
            res.status(500).json({ error: 'Database error' });
        }
    } else {
        console.warn('Invalid HTTP method used:', req.method); // Log unexpected methods
        res.status(405).json({ error: 'Method Not Allowed' });
    }
}
