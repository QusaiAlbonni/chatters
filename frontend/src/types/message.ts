import type { User, Message } from "@/api/v1";

export class ExpandableMessage implements Message {

    constructor(
      public content: string,
      public pk?: number | undefined,
      public user?: User | undefined,
      public room?: number | undefined,
      public created_at?: string | undefined,
      public modified_at?: string | undefined,
      public expanded: boolean  = false,
    ){}

    isOwned(userId: number | undefined): boolean{
      return this.user?.id === userId;
    }
}
