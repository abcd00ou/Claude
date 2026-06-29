export type TeamId = "sales" | "marketing" | "product_planning";

export type DraftStatus = "generating" | "ready" | "sent" | "error";

export type SignalTag = "REAL" | "SIM";

/** One daily task-level update — for the leader's in-tab scan panel. */
export interface TaskUpdate {
  category: string;
  tag: SignalTag;
  headline: string;
  detail: string;
  source: string; // citation for REAL; "" for SIM
}

/** Ordered email-body blocks the model composes — natural commentary mixed with
 *  a table where numbers belong and a chart for a trend. */
export type EmailBlock =
  | { type: "text"; text: string }
  | { type: "table"; title?: string; columns: string[]; rows: string[][] }
  | {
      type: "chart";
      title?: string;
      unit?: string; // e.g. "% QoQ", "k units"
      bars: { label: string; value: number; tag?: SignalTag }[];
    };

export interface ReportContent {
  taskUpdates: TaskUpdate[]; // leader's categorized scan panel
  emailBlocks: EmailBlock[]; // the natural CEO email (commentary + table + chart)
}

export interface Draft {
  team: TeamId;
  subject: string;
  content: ReportContent | null;
  html: string; // SK hynix-branded email, rendered from emailBlocks
  status: DraftStatus;
  generatedAt: string;
  sentAt?: string;
  sentSimulated?: boolean; // true = demo "send" with no email provider configured
  error?: string;
  lastFeedback?: string;
}
