import { create } from "zustand";

export const useAppStore = create((set) => ({
  docId: null as string | null,
  setDocId: (id: string) => set({ docId: id }),
}));
