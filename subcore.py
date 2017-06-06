from classes import *

'''
Returns a neat, partial, envy-free alocation of pieces of cake among the agents given

Translation key for variables
Paper -> Code

a[i] -> agents[i].preferred_value


'''
def subcore(pieces, agents):

    print("Calling subcore with",len(pieces),"pieces and",len(agents),'agents')

    #Ensure that no piece passed in was trimmed by an agent passed in
    for p in pieces:
        for t in p.trims:
            assert t.owner not in agents

    # Set all agent favorite piece value in variable a
    for agent in agents:
        agent.preferred_value = agent.get_value( agent.choose_piece(pieces) )


    for m in range(1,len(agents)+1):
        print("m=",m)

        # If the next agent's preferred piece is unallocated
        preferred_piece = agents[m-1].choose_piece(pieces)
        if preferred_piece.allocated == None:
            preferred_piece.allocated = agents[m-1]
        else:
            # m-1 pieces are being contested by m agents
            contested_pieces = list(filter(lambda p: p.allocated != None, pieces))
            uncontested_pieces = list(filter(lambda p: p.allocated == None, pieces))
            assert len(uncontested_pieces) >= 1

            for agent in agents[:m]:
                uncontested_max_value = max(map(agent.get_value, uncontested_pieces))
                print("This agent's uncontested max value is",float(uncontested_max_value))
                for piece in contested_pieces:
                    print("Whereas this piece is worth",float(agent.get_value(piece)))
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



            for agent in agents:
                agent.benchmark = max(map(agent.get_value, uncontested_pieces))
                
            winners = []
            for piece in contested_pieces:
                winner = piece.rightmost_cutter()
                if not winner in winners:
                    winners.append(winner)

            while len(winners) < m-1:
                print("BEGINNING WHILE LOOP")

                # Forget allocations
                # TODO should this go here?
                for piece in pieces:
                    piece.allocated = None

                # Forget previous trims
                for piece in contested_pieces:
                    #Is this safe? VVVV
                    piece.forget_trims_by_agents(winners)

                subcore(contested_pieces, winners)
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

            #TODO is this check useful?
            assert envy_free(contested_pieces)

            subcore(contested_pieces, winners)
            

            losers = list(set(agents[:m]) - set(winners))
            assert len(losers) == 1
            loser = losers[0]
            
            preferred_uncontested_piece = loser.choose_piece(uncontested_pieces)
            preferred_uncontested_piece.allocated = loser

            # TODO Assert that loser prefers this piece to all contested pieces?
        # END IF/ELSE

        # Set all agent favorite piece value
        agent_check = set([])
        for p in pieces:
            if p.allocated != None:
                p.allocated.preferred_value = agent.get_value(p)
                assert p.allocated not in agent_check
                agent_check.add(p.allocated)
        assert agent_check == set(agents[:m])
    #END FOR
    assert envy_free(pieces)
    return pieces
