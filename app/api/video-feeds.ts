import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    const response = await fetch('http://localhost:5003/video_feed');
    if (response.ok) {
      res.writeHead(200, {
        'Content-Type': 'multipart/x-mixed-replace; boundary=frame',
      });
      response.body?.pipe(res); // Stream the video feed
    } else {
      res.status(response.status).send(`Error: ${response.statusText}`);
    }
  } catch (error: any) {
    res.status(500).send(`Error: ${error.message}`);
  }
}


