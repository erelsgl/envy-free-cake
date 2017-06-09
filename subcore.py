from classes import *
from debug import *


'''
Returns a neat, partial, envy-free alocation of pieces of cake among the agents given

Translation key for variables
Paper -> Code

a[i] -> agents[i].preferred_value


'''
def subcore(pieces, agents, call_signature=""):
    debug_print()
    debug_print(call_signature)
    debug_print("Calling subcore with",len(pieces),"pieces and",len(agents),'agents')

    #Ensure that no piece passed in was trimmed by an agent passed in
    for p in pieces:
        for t in p.trims:
            assert t.owner not in agents

    # Set all agent favorite piece value in variable a
    # TODO cache agent values
    for agent in agents:
        agent.preferred_value = agent.get_value( agent.choose_piece(pieces) )


    for m in range(1,len(agents)+1):
        debug_print("m=",m)



        # If the next agent's preferred piece is unallocated
        # IMPORTANT: This line breaks our previous upper bound for the operation of sub_core, becaus
        preferred_piece = agents[m-1].choose_piece(pieces)
        if preferred_piece.allocated == None:
            preferred_piece.allocated = agents[m-1]
        else:
            # m-1 pieces are being contested by m agents
            contested_pieces = list(filter(lambda p: p.allocated != None, pieces))
            uncontested_pieces = list(filter(lambda p: p.allocated == None, pieces))
            assert len(uncontested_pieces) >= 1

            #This assertion "never makes sense" --Christian Bechler, 2017-06-06 12:20 EST
            #assert all([p.rightmost_cutter() not in agents[:m] for p in contested_pieces])

            for agent in agents[:m]:
                #TODO replace these get_value calls with cached value checking
                uncontested_max_value = max( [agent.get_value(p) for p in uncontested_pieces] )
                debug_print(agent, "uncontested max value is",float(uncontested_max_value))
                for piece in contested_pieces:
                    debug_print("Whereas",piece,"is worth",float(agent.get_value(piece, count=False)))
                    #Because new valuations are made from the rightmost trim, don't immediately add these new trims to the piece.
                    possible_trim =  agent.get_trim_of_value(piece, uncontested_max_value)
                    if possible_trim != None:
                        piece.pending_trims.append(possible_trim)

            #TODO should this be its own method in Piece class?
            #Now add the pending trims to the actual trims
            for piece in contested_pieces:
                piece.trims.extend(piece.pending_trims)
                #Make sure the trims are sorted by their x position
                piece.trims = sorted(piece.trims, key = lambda t: t.x)
                piece.pending_trims = []


            #Kenan asks why benchmarks are even necessary
            #They don't modify the flow of code at all, but they're used in the proof
            #TODO replace this with cached value checks
            for agent in agents:
                agent.benchmark = max( [agent.get_value(p) for p in uncontested_pieces] )
                
            winners = []
            for piece in contested_pieces:
                winner = piece.rightmost_cutter()

                '''
                There might be no trims on the piece, in which case it is None
                The rightmost trim may be from a higher call of subcore
                We only place each winner in the list once
                '''
                if winner != None and \
                        winner in agents[:m] and \
                        winner not in winners:
                    winners.append(winner)

            while len(winners) < m-1:
                debug_print("BEGINNING WHILE LOOP")

                # Forget allocations
                # TODO should this go here?
                for piece in pieces:
                    piece.allocated = None

                # Forget previous trims
                for piece in contested_pieces:
                    #Is this safe? VVVV
                    piece.forget_trims_by_agents(winners)

                subcore(contested_pieces, winners, call_signature = call_signature+' m'+str(m)+'w')

                unallocated_contested_piece = list(filter(lambda p: p.allocated == None, contested_pieces)) [0]
                new_winner = unallocated_contested_piece.rightmost_cutter()
                assert new_winner != None
                unallocated_contested_piece.allocated = new_winner
                winners.append( new_winner )
            #END WHILE

            # Forget previous trims
            for piece in contested_pieces:
                #Is this safe? VVVV
                piece.forget_trims_by_agents(winners)
                ##????
                piece.allocated = None

            subcore(contested_pieces, winners, call_signature = call_signature+' m'+str(m))
            
            losers = list(set(agents[:m]) - set(winners))
            ##TODO DEBUG REMOVE!!!!
            if len(losers) != 1:
                debug_print("Winners are:",winners)
                debug_print("Losers  are:",losers)
                debug_print("Agents[:m] :",agents[:m])
                assert False

            loser = losers[0]
            
            preferred_uncontested_piece = loser.choose_piece(uncontested_pieces)
            preferred_uncontested_piece.allocated = loser

            # TODO Assert that loser prefers this piece to all contested pieces?
        # END IF/ELSE

        # Set all agent favorite piece value
        agent_check = set([])
        for p in pieces:
            if p.allocated != None:
                p.allocated.preferred_value = agent.get_value(p, count=False)
                assert p.allocated not in agent_check
                agent_check.add(p.allocated)
        assert agent_check == set(agents[:m])
    #END FOR
    assert envy_free(pieces)
    #This next assertion about benchmarks should be implied by envy_free above, but this is useful to remember for the proof:
    for a in agents:
        assert a.benchmark <= a.get_value(a.choose_piece(pieces, count=False), count=False)
    debug_print("Returning from subcore with",len(pieces),"pieces and",len(agents),'agents')
    debug_print()
    return pieces
