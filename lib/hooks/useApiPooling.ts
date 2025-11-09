import { useState, useEffect } from 'react';

type ApiFunction<T> = () => Promise<T>;

export function useApiPolling<T>(apiFunction: ApiFunction<T>, delay: number): T | null {
    const [data, setData] = useState<T | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiFunction();
                setData(response);
            } catch (error) {
                console.error(error);
            }
        };

        const intervalId = setInterval(fetchData, delay);

        // Clear the interval on unmount
        return () => clearInterval(intervalId);
    }, [apiFunction, delay]);

    return data;
}