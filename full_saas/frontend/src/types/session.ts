export type CognitiveSession = {
  id?: number;
  anonymous_id: string;
  session_date?: string;
  sleep_quality: number;
  stress: number;
  alertness: number;
  digit_span: number;
  reaction_time_ms: number;
  stroop_accuracy: number;
  stroop_interference_ms: number;
  notes: string;
  opt_in_sync: boolean;
};
