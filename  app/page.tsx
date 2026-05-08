import Link from 'next/link'

export default function Home() {
  return (
    <main className="p-8 md:p-12 max-w-6xl mx-auto">
      <div className="card p-8 md:p-12">
        <p className="text-cyan-300 font-semibold">Edge Tech Knowledgey</p>
        <h1 className="text-4xl md:text-6xl font-black mt-4 leading-tight">
          PhoneServe network control with a high-tech launch portal.
        </h1>
        <p className="mt-4 text-slate-300 max-w-2xl">
          Manage nodes, capture leads, and present IronSkin in a polished investor-ready environment.
        </p>
        <div className="mt-8 flex gap-3 flex-wrap">
          <Link className="btn" href="/dashboard">
            Open Dashboard
          </Link>
          <Link className="btn" href="/admin">
            Open Admin
          </Link>
          <Link className="btn" href="/ironskin">
            IronSkin Specs
          </Link>
        </div>
      </div>
    </main>
  )
}