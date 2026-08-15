import api from "@/libs/axios";
import { IncidentCreatePayload } from "@/schemas/incident.schema";
import {
  SignatureAPIRequest,
  SignatureResponse,
  UploadedMedia,
} from "@/types/incident.type";
import { uploadToCloudinary } from "@/utils/uploadToCloudinary";

export class IncidentService {
  //   For getting signature to uplaod image in cloudinary
  static getSignatures = async (
    data: SignatureAPIRequest,
  ): Promise<SignatureResponse> => {
    const res = await api.post("/ap1/v1/incident/media/signatures", data);
    return res.data.data;
  };
  static handleImageUpload = async (
    data: IncidentCreatePayload,
  ): Promise<UploadedMedia[]> => {
    const file_types: Array<"image" | "audio"> = [];
    const allFiles = [];
    if (data.images) {
      allFiles.push(...data.images);
      for (let i = 0; i < data.images.length; i++) {
        file_types.push("image");
      }
    }
    if (data.audio) {
      file_types.push("audio");
      allFiles.push(data.audio);
    }
    const file_length = allFiles.length;
    if (file_length > 0) {
      try {
        const signatures = await IncidentService.getSignatures({
          file_length,
          file_types,
        });
        const results = [];
        for (let i = 0; i <= file_length - 1; i++) {
          const uploadResponse = await uploadToCloudinary(
            allFiles[i],
            signatures.signatures[i],
          );
          const resultData = {
            type: uploadResponse.resource_type,
            url: uploadResponse.url,
            meta_data: {
              public_id: uploadResponse.public_id,
              url: uploadResponse.url,
              format: uploadResponse.format,
              size: uploadResponse.bytes / 1024,
              width: uploadResponse.width,
              height: uploadResponse.height,
            },
          };
          results.push(resultData);
        }
        return results;
      } catch (error) {
        console.log(error);
      }
    }
    return [];
  };
}
