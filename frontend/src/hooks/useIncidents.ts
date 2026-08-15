import api from "@/libs/axios";
import { SuccessResponse } from "@/types/common";
import { IncidentRequest } from "@/types/incident.type";
import { useMutation } from "@tanstack/react-query";

export const useCreateIncident = () => {
  return useMutation<SuccessResponse<null>, Error, IncidentRequest>({
    mutationFn: async (data) => {
      const res = await api.post("/api/v1/sos/incident/", data);
      return res.data;
    },
  });
};
