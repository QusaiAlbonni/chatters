import type { User, Message } from "@/api/v1";
import { useTransStore } from "@/stores/translation";

export class ExpandableMessage implements Message {

    constructor(
      public content: string,
      public pk?: number | undefined,
      public user?: User | undefined,
      public room?: number | undefined,
      public created_at?: string | undefined,
      public modified_at?: string | undefined,
      public expanded: boolean  = false,
      public language: string = 'en',
      public translations: any = {},
    ){}

    isOwned(userId: number | undefined): boolean{
      return this.user?.id === userId;
    }

    get translatedContent(): string{
      const transStore= useTransStore();
      const lang = transStore.lang
      let content = this.content;
      if (lang in this.translations){
        content = this.translations[lang];
      }
      return content
    }
}
