'use client'

import { useState } from "react";
import {z} from 'zod'

const urlSchema = z.url({ message: "Please enter a valid URL" });
const delay = (ms:number) => new Promise(resolve => setTimeout(resolve, ms));

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('')
  const [url, seturl] = useState('')


  const handle_button = async (e:React.MouseEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    await delay(600)
    const parsed = urlSchema.safeParse(url)

    if (!parsed.success){
      setError(parsed.error.issues[0].message || "Please enter a valid URL")
      setLoading(false)
    }
  }


  return (
    <div className="w-full min-h-screen font-mono bg-white flex flex-col">
      <div className="min-h-screen flex flex-col">
        <header className="w-full flex flex-col p-6 pb-2">
          {/* Logo */}
          <h1 className="text-[32px] text-[#161616] font-medium font-mono">
            rawrecipe
          </h1>
        </header>

        <div className="w-full -mt-12 flex-1 h-full flex flex-col items-center justify-center p-4">
          <div className={`flex flex-row w-full max-w-lg items-center border-2 rounded-[3px] overflow-hidden text-[20px] transition-colors duration-200 ${
            loading 
              ? "border-[#161616]/60 bg-gray-50 text-[#161616]/60" 
              : "border-[#161616]/90 text-[#161616]"
          }`}>
            
            <input 
              placeholder={loading ? "Scraping recipe data..." : "Enter your recipe Url here"} 
              value={url}
              onChange={(e)=>seturl(e.target.value)}
              type="text" 
              disabled={loading}
              className="outline-hidden px-4 py-4 bg-transparent grow min-w-0 placeholder:text-[#161616]/80 disabled:cursor-progress"
            />

            <button 
              onClick={(e) => {
                e.preventDefault(); 
                setLoading(true); 
                handle_button(e)
              }} 
              disabled={loading}
              className={`h-full aspect-square flex items-center justify-center p-4 text-white shrink-0 transition-colors duration-200 ${
                loading 
                  ? "bg-[#161616]/60 cursor-progress" 
                  : "bg-[#161616]/90 cursor-pointer"
              }`}
            >
              <span>{loading ? "BBB" : "AAA"}</span>
            </button>
            
            
          </div>
          <div className="inline max-w-lg w-full mt-2 text-[20px] text-[#C11919] text-left  ">
          <span>{error}</span>
          <span className="text-transparent">'</span>
          </div>

        </div>
      </div>
    </div>
  );
}