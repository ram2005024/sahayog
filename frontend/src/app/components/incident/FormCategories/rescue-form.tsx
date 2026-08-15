"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  IncidentCreateForm,
  IncidentCreatePayload,
} from "@/schemas/incident.schema";

import { UseFormReturn } from "react-hook-form";

type RescueFormProps = {
  form: UseFormReturn<IncidentCreateForm, unknown, IncidentCreatePayload>;
};

const RescueForm: React.FC<RescueFormProps> = ({ form }) => {
  // Narrow errors to the rescue branch
  const rescueErrors = form.formState.errors.details as {
    no_of_peoples_affected?: { message?: string };
    no_of_volunteers_required?: { message?: string };
    life_threat?: { message?: string };
  };

  return (
    <div className="space-y-4">
      <Field>
        <FieldLabel>People Affected</FieldLabel>
        <Input
          type="number"
          {...form.register("details.no_of_peoples_affected", {
            valueAsNumber: true,
          })}
        />
        <FieldError>{rescueErrors?.no_of_peoples_affected?.message}</FieldError>
      </Field>

      <Field>
        <FieldLabel>Volunteers Required</FieldLabel>
        <Input
          type="number"
          {...form.register("details.no_of_volunteers_required", {
            valueAsNumber: true,
          })}
        />
        <FieldError>
          {rescueErrors?.no_of_volunteers_required?.message}
        </FieldError>
      </Field>
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
        <FieldError>
          {form.formState.errors.details?.life_threat?.message}
        </FieldError>
      </Field>
    </div>
  );
};

export default RescueForm;
