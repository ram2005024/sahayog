import z from "zod";

// Rescue Schema
const RescueSchema = z.object({
  type: z.literal("rescue"),
  no_of_peoples_affected: z.number().int().positive(),
  no_of_volunteers_required: z.number().int().positive(),
  life_threat: z.boolean(),
});

// Medical Schema
const MedicalSchema = z.object({
  type: z.literal("medical"),
  ambulance_required: z.boolean(),
  doctors_required: z.boolean(),
  life_threat: z.boolean(),
  blood_required: z.boolean(),
});

export const IncidentCreateSchema = z.object({
  heading: z.string().min(4, "Must have atleast 4 characters"),
  description: z.string().optional(),
  user_profile_id: z.string().optional(),
  priority: z.enum(["high", "critical", "medium"]),
  location_description: z.string().min(4, "Must have atleast 4 characters"),
  latitude: z
    .string()
    .min(1, "Latitude is required")
    .transform((val) => parseFloat(val)),
  longitude: z
    .string()
    .min(1, "Longitude is required")
    .transform((val) => parseFloat(val)),

  // Files
  images: z
    .array(z.instanceof(File))
    .max(3, "Maximum 3 images allowed")
    .optional(),
  audio: z.instanceof(File).optional(),

  details: z.discriminatedUnion("type", [RescueSchema, MedicalSchema]),
});

export type IncidentCreateForm = z.input<typeof IncidentCreateSchema>;

export type IncidentCreatePayload = z.output<typeof IncidentCreateSchema>;
