//import Image from 'next/image'

const teamMembers = [
  {
    name: "Khansa Farras Callista Armandsyah",
    university: "Universitas Negeri Jakarta - Fisika",
    role: "Machine Learning Cohort"
  },
  {
    name: "Adrian Alfajri",
    university: "Universitas Trisakti - Informatika",
    role: "Machine Learning Cohort"
  },
  {
    name: "Adyatma Imam Susanto",
    university: "UPN Veteran Jawa Timur - Informatika",
    role: "Machine Learning Cohort"
  },
  {
    name: "Mohamad Ifdhal Hassan Noor",
    university: "Institut Pertanian Bogor - Fisika",
    role: "Machine Learning Cohort"
  },
  {
    name: "Ananda Sheva Hidayat",
    university: "Universitas Lampung - Ilmu Komputer",
    role: "Cloud Computing Cohort"
  },
  {
    name: "Alverta Orlandia Prijono",
    university: "Politeknik Negeri Jakarta - Teknik Elektro",
    role: "Cloud Computing Cohort"
  },
]

export default function About() {
  return (
    <div className="py-20 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-12">About Us</h1>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {teamMembers.map((member, index) => (
            <div key={index} className="bg-gray-100 p-6 rounded-lg">
              <div className="w-16 h-16 bg-[#362222] rounded-full mb-4" />
              <h2 className="text-xl font-bold mb-2">{member.name}</h2>
              <p className="text-gray-600 mb-2">{member.university}</p>
              <p className="text-gray-600">{member.role}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

