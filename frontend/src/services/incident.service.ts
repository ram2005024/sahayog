import api from "@/libs/axios";
import { SignatureAPIRequest, SignatureResponse } from "@/types/incident.type";

export class IncidentService {
  //   For getting signature to uplaod image in cloudinary
  static getSignatures = async (
    data: SignatureAPIRequest,
  ): Promise<SignatureResponse> => {
    const res = await api.post("/ap1/v1/incident/media/signatures", data);
    return res.data.data;
  };
}
