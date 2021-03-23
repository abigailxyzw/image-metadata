import argparse
import os
from parse_json import parse_json
from utils import split_by_tripcode
from visualizations import plot_dow, plot_hod

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Print time of day and day of week data for the Q posts')

    parser.add_argument('--reformat_json', action='store_true', help='Reformat the json input as a tsv file (does not include the text of the drops themselves).')
    parser.add_argument('--split_by_tripcode', action='store_true', help='Split parsed qanon input by tripcode. Assumes --reformat_json has already been called.')
    parser.add_argument('--make_bar_graphs', action='store_true', help='Produces bargraphs and analysis to show hour of day and day of week drop patterns. Call --reformat_json and --split_by_tripcode first.')
    args=parser.parse_args()


    reformat=args.reformat_json
    bar_graphs=args.make_bar_graphs
    tripcode=args.split_by_tripcode
    

    if reformat:
        print("Reformatting json")
        parse_json()
 
    elif bar_graphs:
        print("Making bar graphs")
        plot_dow()
        plot_hod()

    elif tripcode:
        print("Splitting input by tripcode")
        split_by_tripcode()
    
    else:
        print("Reformatting json")
        parse_json()
        print("Splitting by tripcode")
        split_by_tripcode()
        print("Making bar graphs")
        plot_dow()
        plot_hod()



    
    
    


    

    
   
