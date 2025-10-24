import Image from "next/image";
import FileUploader from "../components/FileUploader";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex min-h-screen w-full max-w-3xl flex-col items-center justify-between py-16 px-6 bg-white dark:bg-black sm:items-start">
        <div className="w-full flex items-center justify-center py-6">
          <Image
            className="dark:invert"
            src="/next.svg"
            alt="Next.js logo"
            width={100}
            height={20}
            priority
          />
        </div>

        <div className="flex w-full flex-col items-center gap-6 text-center sm:items-start sm:text-left">
          <h1 className="max-w-xs text-2xl font-semibold leading-8 tracking-tight text-black dark:text-zinc-50">
            Attach a document
          </h1>
          <p className="max-w-md text-sm leading-7 text-zinc-600 dark:text-zinc-400">
            Use the control below to attach a PDF or Word document. This is a client-side
            input with basic validation. To actually upload the file, add an API route
            and wire the upload logic.
          </p>

          <div className="mt-4 w-full">
            <FileUploader />
          </div>
        </div>

        <div className="mt-8 flex w-full flex-col gap-4 text-base font-medium sm:flex-row">
          <a
            className="flex h-12 w-full items-center justify-center gap-2 rounded-full bg-foreground px-5 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc] md:w-[158px]"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy Now
          </a>
          <a
            className="flex h-12 w-full items-center justify-center rounded-full border border-solid border-black/[.08] px-5 transition-colors hover:border-transparent hover:bg-black/[.04] dark:border-white/[.145] dark:hover:bg-[#1a1a1a] md:w-[158px]"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Documentation
          </a>
        </div>
      </main>
    </div>
  );
}
