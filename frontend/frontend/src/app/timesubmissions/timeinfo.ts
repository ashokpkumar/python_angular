import { project } from "../add-projects/projects"
import { projectManager } from "../projects/assignPM"

export class timeSubmissions{
    date:string
    username:string
    managername:string
    timetype:string
    hours:string
    approved:boolean
    submission_id:string
  }
  export enum users{
    admin="admin",
    manager="manager",
    vp="vp",
    rmgadmin="rmg admin",
    projectManager="project manager"
  }
  