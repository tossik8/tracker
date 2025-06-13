import math

import argparse

from .db import Database


def start_session(args, db: Database):
    project_id = db.get_project_id_by_name(args.project)
    if project_id is None:
        project_id = db.insert_project(args.project)
        db.insert_session(project_id)
    else:
        active_session = db.get_active_session_id_by_project_id(project_id[0])
        if active_session is not None:
            raise ValueError(f"Cannot start a new session. Project '{args.project}' has an active session.")
        db.insert_session(project_id[0])
    print("Session started.")
        

def stop_session(args, db: Database):
    project_id = db.get_project_id_by_name(args.project)
    if project_id is None:
        raise ValueError(f"Project '{args.project}' does not exist.")
    active_session = db.get_active_session_id_by_project_id(project_id[0])
    if active_session is None:
        raise ValueError("There are no active sessions to stop.")
    db.set_session_end(active_session[0])
    finished_session = db.get_session_by_id(active_session[0])
    print(f"Project '{args.project}'. Session lasted {finished_session[2] - finished_session[1]}.")


def report_activity(args, db: Database):
    project_id = db.get_project_id_by_name(args.project)
    if project_id is None:
        raise ValueError(f"Project '{args.project}' does not exist.")
    analytics = db.get_project_analytics(project_id[0])
    hours = analytics[1] * 24
    minutes = (hours * 60) % 60
    seconds = (minutes * 60) % 60
    print(
        f"Sessions: {analytics[0]}.\n" \
        f"Time spent: {math.floor(analytics[1])} days, {math.floor(hours)}:{math.floor(minutes)}:{math.floor(seconds)}."
    )


def list_projects(_, db: Database):
    projects = db.get_projects()
    for project in projects:
        print(project)
    print(f"Projects: {len(projects)}.")


def delete_project(args, db: Database):
    project_id = db.get_project_id_by_name(args.project)
    if project_id is None:
        raise ValueError(f"Project '{args.project}' does not exist.")
    db.delete_project(project_id[0])
    print("Project deleted.")


def main():    
    parser = argparse.ArgumentParser("tracker")
    subparsers = parser.add_subparsers(required=True)
    start_subparser = subparsers.add_parser("start")
    start_subparser.add_argument("project")
    start_subparser.set_defaults(func=start_session)

    stop_subparser = subparsers.add_parser("stop")
    stop_subparser.add_argument("project")
    stop_subparser.set_defaults(func=stop_session)

    report_subparser = subparsers.add_parser("report")
    report_subparser.add_argument("project")
    report_subparser.set_defaults(func=report_activity)

    list_subparser = subparsers.add_parser("list")
    list_subparser.set_defaults(func=list_projects)

    delete_subparser = subparsers.add_parser("delete")
    delete_subparser.add_argument("project")
    delete_subparser.set_defaults(func=delete_project)

    args = parser.parse_args()
    db = Database()
    try:
        args.func(args, db)
    except ValueError as e:
        print(e)
