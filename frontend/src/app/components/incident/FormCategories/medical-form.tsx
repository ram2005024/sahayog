"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import {
  IncidentCreateForm,
  IncidentCreatePayload,
} from "@/schemas/incident.schema";
import { UseFormReturn } from "react-hook-form";

type MedicalFormProps = {
  form: UseFormReturn<IncidentCreateForm, unknown, IncidentCreatePayload>;
};

const MedicalForm: React.FC<MedicalFormProps> = ({ form }) => {
  const errors = form.formState.errors.details as {
    ambulance_required?: { message?: string };
    doctors_required?: { message?: string };
    life_threat?: { message?: string };
    blood_required?: { message?: string };
  };

  return (
    <div className="space-y-4 gap-4 grid grid-cols-2">
      {/* Ambulance Required */}
      <Field>
        <FieldLabel>Ambulance Required</FieldLabel>
        <div className="flex space-x-6">
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.ambulance_required") === true}
              onCheckedChange={() =>
                form.setValue("details.ambulance_required", true)
              }
            />
            <span>Yes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.ambulance_required") === false}
              onCheckedChange={() =>
                form.setValue("details.ambulance_required", false)
              }
            />
            <span>No</span>
          </div>
        </div>
        <FieldError>{errors?.ambulance_required?.message}</FieldError>
      </Field>

      {/* Doctors Required */}
      <Field>
        <FieldLabel>Doctors Required</FieldLabel>
        <div className="flex space-x-6">
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.doctors_required") === true}
              onCheckedChange={() =>
                form.setValue("details.doctors_required", true)
              }
            />
            <span>Yes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.doctors_required") === false}
              onCheckedChange={() =>
                form.setValue("details.doctors_required", false)
              }
            />
            <span>No</span>
          </div>
        </div>
        <FieldError>{errors?.doctors_required?.message}</FieldError>
      </Field>

      {/* Life Threat */}
      <Field>
        <FieldLabel>Life Threat</FieldLabel>
        <div className="flex space-x-6">
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.life_threat") === true}
              onCheckedChange={() => form.setValue("details.life_threat", true)}
            />
            <span>Yes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.life_threat") === false}
              onCheckedChange={() =>
                form.setValue("details.life_threat", false)
              }
            />
            <span>No</span>
          </div>
        </div>
        <FieldError>{errors?.life_threat?.message}</FieldError>
      </Field>

      {/* Blood Required */}
      <Field>
        <FieldLabel>Blood Required</FieldLabel>
        <div className="flex space-x-6">
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.blood_required") === true}
              onCheckedChange={() =>
                form.setValue("details.blood_required", true)
              }
            />
            <span>Yes</span>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox
              checked={form.watch("details.blood_required") === false}
              onCheckedChange={() =>
                form.setValue("details.blood_required", false)
              }
            />
            <span>No</span>
          </div>
        </div>
        <FieldError>{errors?.blood_required?.message}</FieldError>
      </Field>
    </div>
  );
};

export default MedicalForm;
