import getAllVehicleStats from "@/actions/getAllVehiceStats";
import VehicelStatsTable from "@/components/VehicelStatsTable";

export type VehicleStatsResponse = {
    count_id: number,
    timestamp: string,
    location: string,
    car_count: number,
    motorbike_count: number,
    truck_count: number,
    bus_count: number
}


export default async function History() {

    const res = await getAllVehicleStats() as VehicleStatsResponse[] || [];

    if (res.length == 0) {
        return <h1>No data</h1>
    } else {
        return (
            <div className="py-24 px-4">
                <div className="max-w-6xl mx-auto">
                    <h1 className="text-4xl font-bold text-center mb-12-">History</h1>
                    <VehicelStatsTable data={res} />
                </div>
            </div>
        )
    }
}
