'use client'
import { useRef, useState } from "react";
import {z} from 'zod'
import { useTheme } from "@/components/ThemeProvider"
const urlSchema = z.url({ message: "Please enter a valid URL" });
const delay = (ms:number) => new Promise(resolve => setTimeout(resolve, ms));

interface ParsedIngredient{
  text:string,
  quantity:string,
  unit:string,
  name:string
}


interface Recipe {
  title: string;
  author: string | null;
  ingredients: ParsedIngredient[];
  instructions: Array<{ name: string; text: string }>;
  yields: string | null;
  image: string | any;
}

export default function Home() {
  const {resolvedTheme, setTheme } = useTheme();  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('')
  const [url, seturl] = useState('')
  const [recipe, setRecipe] = useState<Recipe | null>(null)
  const recipeSectionRef = useRef<HTMLDivElement>(null);


  const handle_button = async (e:React.MouseEvent) => {
    e.preventDefault()
    setError('')

    await delay(600)
    const parsed = urlSchema.safeParse(url)

    if (!parsed.success){
      setError(parsed.error.issues[0].message || "Please enter a valid URL")
      setLoading(false)
      return
    }

    try{ 
      const targetUrl = `http://${process.env.NEXT_PUBLIC_API_URL}/scrape_recipe?url=${encodeURIComponent(url)}`;
      const response = await fetch(targetUrl, {
        method:"GET",
        headers:{
          'Content-Type': 'application/json',        
        }
      })

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to scrape recipe.");
      }

      const data = await response.json();
      setRecipe(data)
      setTimeout(() => {
        recipeSectionRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);

    }
    catch(err:any){
      setError(err.message || "an error occured")
    }
    finally{
      setLoading(false)
    }
  }



  return (
    <div className="w-full min-h-screen font-mono bg-white text-[#161616] dark:bg-[#121212] dark:text-white transition-colors duration-200 flex flex-col">
      <div className="min-h-screen flex flex-col">
        <header className="w-full flex flex-row justify-between p-6 pb-2">
          {/* Logo */}
          <h1 className="text-[32px] text-[#161616] dark:text-zinc-200 font-medium font-mono">
            rawrecipe
          </h1>
          <button 
            onClick={() => {setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}}          className="border border-[#161616] z-50 dark:border-white px-4 rounded-[2px] text-sm cursor-pointer hover:bg-gray-100 dark:hover:bg-zinc-800 transition-colors"
          >

              {resolvedTheme === 'dark' ? 'LIGHT' : 'DARK'}     

          </button>
        </header>

        <div className="w-full -mt-12 flex-1 h-full flex flex-col items-center justify-center p-4">
          <div className={`flex flex-row w-full max-w-lg items-center border-2 rounded-[3px] overflow-hidden text-[20px] transition-colors duration-200 ${
            loading 
              ? "border-[#161616]/60 bg-gray-50 text-[#161616]/60 dark:text-zinc-500 dark:border-zinc-700 dark:bg-zinc-900" 
              : "border-[#161616]/85 text-[#161616] dark:border-zinc-600 dark:text-zinc-200"
          }`}>
            
            <input 
              placeholder={loading ? "Scraping recipe data..." : "Enter your recipe Url here"} 
              value={url}
              onChange={(e)=>seturl(e.target.value)}
              type="text" 
              disabled={loading}
              className="outline-hidden px-4 py-4 bg-transparent grow min-w-0 placeholder:text-[#161616]/80 dark:placeholder:text-zinc-400 disabled:cursor-progress"
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
                  ? "bg-[#161616]/60 text-white  cursor-progress" 
                  : "bg-[#161616]/85 text-white dark:bg-zinc-600 cursor-pointer"
              }`}
            >
              <span>{loading ? "BBB" : "AAA"}</span>
            </button>
            
            
          </div>
          <div className="inline max-w-lg w-full mt-2 text-[20px] text-[#C11919] dark:text-red-400 text-left  ">
          <span>{error}</span>
          <span className="text-transparent">'</span>
          </div>

        </div>
      </div>
      
       <div className="w-full min-h-screen flex-1 h-full pt-8 pl-8 flex text-[#161616] dark:text-white  flex-col items-center justify-center p-4">
         
              {recipe && (
                <div ref={recipeSectionRef} className=" pt-8 dark:text-zinc-200 text-left w-full h-full flex-1 max-w-lg">
                  <h1 className="text-[32px] text-[#161616] dark:text-zinc-200 font-medium">{recipe.title}</h1>
                  <h3 className="text-[24.6px] font-medium mt-2">Ingredients:</h3>
                  <ul className=" list-none pl-5 text-[20px]">
                    {recipe.ingredients.map((ing: any, i: number) => (
                      <li className=" before:content-['-'] before:mr-2 " key={i}>{ing.quantity} {ing.unit} {ing.name}</li>
                    ))}
                  </ul>

                  <h3 className="text-[24.6px] font-medium mt-4">Instructions:</h3>
                  <ul className="list-none pl-5 text-[20px]">
                    {recipe.instructions.map((inst: any, i: number) => (
                      <li className="before:content-['-'] before:mr-2 mb-2" key={i}>{inst.text}</li>
                    ))}
                  </ul>

                </div>
              )}
        </div>
    </div> 
  );
}