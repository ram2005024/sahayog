"use client";
import api from "@/libs/axios";
import { IncidentCreatePayload } from "@/schemas/incident.schema";
import {
  SignatureAPIRequest,
  SignatureResponse,
  UploadedMedia,
} from "@/types/incident.type";
import { uploadToCloudinary } from "@/utils/uploadToCloudinary";
import imageCompression from "browser-image-compression";
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
        const compressedFiles = await Promise.all(
          allFiles.map((file) => {
            // skip compression for <1MB
            if (file.size < 1024 * 1024) return file;
            return imageCompression(file, {
              maxSizeMB: 1,
              maxWidthOrHeight: 1080,
              useWebWorker: true,
            });
          }),
        );

        const uploadPromises = compressedFiles.map((file, i) =>
          uploadToCloudinary(file, signatures.signatures[i]),
        );

        const uploadResponses = await Promise.all(uploadPromises);

        const results = uploadResponses.map((uploadResponse) => ({
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
        }));
        return results;
      } catch (error) {
        console.log(error);
      }
    }
    return [];
  };
}
