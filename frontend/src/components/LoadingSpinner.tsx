import { Loader2 } from "lucide-react";

export function LoadingSpinner({ label = "Carregando..." }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-slate-400">
      <Loader2 className="h-8 w-8 animate-spin text-clinic-500" />
      <p className="mt-3 text-sm">{label}</p>
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div className="py-16 text-center text-sm text-slate-400">{message}</div>
  );
}
