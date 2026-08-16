/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import {
  IncidentCreateForm,
  IncidentCreatePayload,
  IncidentCreateSchema,
} from "@/schemas/incident.schema";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { useCreateIncident } from "@/hooks/useIncidents";
import { IncidentService } from "@/services/incident.service";
import { ErrorResponse } from "@/types/common";
import { UploadedMedia } from "@/types/incident.type";
import { AxiosError } from "axios";
import Image from "next/image";
import { useState } from "react";
import { toast } from "sonner";
import MedicalForm from "./FormCategories/medical-form";
import RescueForm from "./FormCategories/rescue-form";

export default function IncidentForm() {
  const [loadingLocation, setLoadingLocation] = useState<boolean>(false);
  const form = useForm<IncidentCreateForm, unknown, IncidentCreatePayload>({
    resolver: zodResolver(IncidentCreateSchema),
    defaultValues: {
      heading: "",
      description: "",
      user_profile_id: "",
      priority: "medium",
      location_description: "",
      latitude: "",
      longitude: "",
      details: {
        type: "rescue",
        no_of_peoples_affected: 1,
        no_of_volunteers_required: 1,
        life_threat: false,
      },
    },
  });

  const detailsType = useWatch({
    control: form.control,
    name: "details.type",
  });
  const priorityType = useWatch({
    control: form.control,
    name: "priority",
  });
  const lat = useWatch({
    control: form.control,
    name: "latitude",
  });
  const lon = useWatch({
    control: form.control,
    name: "longitude",
  });
  const images = useWatch({
    control: form.control,
    name: "images",
  });
  const audio = useWatch({
    control: form.control,
    name: "audio",
  });
  const handleGetLocation = () => {
    if (!navigator.geolocation) {
      form.setError("latitude", { message: "Geolocation not supported" });
      form.setError("longitude", { message: "Geolocation not supported" });
      return;
    }
    setLoadingLocation(true);

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        form.setValue("latitude", String(pos.coords.latitude));
        form.setValue("longitude", String(pos.coords.longitude));
        form.clearErrors(["latitude", "longitude"]);
        setLoadingLocation(false);
      },

      () => {
        form.setError("latitude", {
          message: "Location permission required",
        });
        form.setError("longitude", {
          message: "Location permission required",
        });
        setLoadingLocation(false);
      },
      { enableHighAccuracy: true },
    );
  };
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files ? Array.from(e.target.files) : [];
    if (files.length > 3) {
      alert("Maximum 3 images allowed");
      e.target.value = "";
      return;
    }
    form.setValue("images", files);
  };

  const handleAudioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      form.setValue("audio", file);
    }
  };
  const createIncidentMutation = useCreateIncident();
  const handleFormSubmit = async (data: IncidentCreatePayload) => {
    let mediaData: UploadedMedia[] = [];
    if (data.images || data.audio) {
      mediaData = await IncidentService.handleImageUpload(data);
    }
    const { images, audio, ...rest } = data;
    createIncidentMutation.mutate(
      { ...rest, medias: mediaData },
      {
        onSuccess: (data) => {
          toast.success(data.message);
          form.reset();
        },
        onError: (err) => {
          const error = err as AxiosError<ErrorResponse<null>>;
          toast.error(
            error.response?.data?.message ||
              error.message ||
              "Something went wrong",
          );
        },
      },
    );
  };

  return (
    <form
      onSubmit={form.handleSubmit(handleFormSubmit)}
      className="space-y-6 max-w-lg mx-auto p-6 border rounded-md shadow-sm"
    >
      {/* Heading */}
      <Field>
        <FieldLabel htmlFor="heading">Heading</FieldLabel>
        <Input
          id="heading"
          {...form.register("heading")}
          placeholder="Incident heading"
        />
        <FieldError>{form.formState.errors.heading?.message}</FieldError>
      </Field>
      {/* Description */}
      <Field>
        <FieldLabel htmlFor="description">Description</FieldLabel>
        <Textarea
          id="description"
          {...form.register("description")}
          placeholder="Incident description"
          className="resize-none"
        />
        <FieldError>{form.formState.errors.description?.message}</FieldError>
      </Field>

      {/* Location */}
      <div className="grid grid-cols-2 gap-4">
        <Field>
          <FieldLabel htmlFor="latitude">Latitude</FieldLabel>
          <Input id="latitude" {...form.register("latitude")} readOnly />
        </Field>
        <Field>
          <FieldLabel htmlFor="longitude">Longitude</FieldLabel>
          <Input id="longitude" {...form.register("longitude")} readOnly />
        </Field>
        {form.formState.errors.longitude && (
          <FieldError>Location must be enabled</FieldError>
        )}
      </div>

      {(!lat || !lon) && (
        <Button
          disabled={loadingLocation}
          type="button"
          onClick={handleGetLocation}
          className="w-full cursor-pointer"
        >
          {loadingLocation ? "Enabling..." : "Enable location"}
        </Button>
      )}
      <Field>
        <FieldLabel htmlFor="location_description">
          Location Description
        </FieldLabel>

        <Input
          id="location_description"
          placeholder="Describe the location"
          {...form.register("location_description")}
        />

        <FieldError>
          {form.formState.errors.location_description?.message}
        </FieldError>
      </Field>

      {/* Images */}
      <Field>
        <FieldLabel htmlFor="images">Upload Images (max 3)</FieldLabel>
        <Input
          id="images"
          type="file"
          accept="image/*"
          multiple
          onChange={handleImageChange}
        />
        <FieldError>{form.formState.errors.images?.message}</FieldError>
      </Field>

      {/* Image Previews */}
      {images && images.length > 0 && (
        <div className="flex gap-2 mt-2">
          {images.map((file, idx) => (
            <Image
              key={idx}
              width={40}
              height={40}
              src={URL.createObjectURL(file)}
              alt={`preview-${idx}`}
              className="w-24 h-24 object-cover rounded"
            />
          ))}
        </div>
      )}

      {/* Audio */}
      <Field>
        <FieldLabel htmlFor="audio">Upload/Record Audio</FieldLabel>
        <Input
          id="audio"
          type="file"
          accept="audio/*"
          capture={true}
          onChange={handleAudioChange}
        />
        <FieldError>{form.formState.errors.audio?.message}</FieldError>
      </Field>

      {/* Audio Preview */}
      {audio && (
        <audio controls className="mt-2 w-full">
          <source src={URL.createObjectURL(audio)} type={audio.type} />
          Your browser does not support the audio element.
        </audio>
      )}
      {/* Priority */}
      <Field>
        <FieldLabel>Priority</FieldLabel>
        <Select
          value={priorityType}
          onValueChange={(val) =>
            form.setValue("priority", val as "high" | "medium" | "critical")
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select priority" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="critical">Critical</SelectItem>
          </SelectContent>
        </Select>
        <FieldError>{form.formState.errors.priority?.message}</FieldError>
      </Field>

      {/* Incident Type */}
      <Field>
        <FieldLabel>Incident Type</FieldLabel>
        <Select
          value={detailsType}
          onValueChange={(val) =>
            form.setValue("details.type", val as "rescue" | "medical")
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="rescue">Rescue</SelectItem>
            <SelectItem value="medical">Medical</SelectItem>
          </SelectContent>
        </Select>
        <FieldError>{form.formState.errors.details?.type?.message}</FieldError>
      </Field>

      {/* Conditional Details */}
      {detailsType === "rescue" && <RescueForm form={form} />}
      {detailsType === "medical" && <MedicalForm form={form} />}

      <Button
        disabled={form.formState.isSubmitting}
        type="submit"
        className="w-full cursor-pointer"
      >
        {form.formState.isSubmitting ? "Saving..." : "Save"}
      </Button>
    </form>
  );
}
