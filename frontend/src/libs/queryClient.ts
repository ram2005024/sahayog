import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // how long data stays fresh
      staleTime: 1000 * 60, // 1 minute
      // retry failed queries once
      retry: 1,
      // don’t refetch when window regains focus
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});
