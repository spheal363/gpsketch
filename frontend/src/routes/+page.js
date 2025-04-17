export async function load({ fetch }) {
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000';
    try {
        const res = await fetch(`${backendUrl}/home`);

        if (!res.ok) {
            console.error('Failed to fetch data from Flask API');
            return { data: null, error: 'Backend is unavailable' };
        }

        const data = await res.json();
        return { data, error: null };
    } catch (err) {
        console.error('Error connecting to backend:', err);
        return { data: null, error: 'Backend is unavailable' };
    }
}