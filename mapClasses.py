import os
import random
import json
import structure as struc

# Map class containing chunks
class Map:

    def __init__(self, app=None):
        self.app = app
        # Chunklist, 2D array consisting of 2D arrays (Chunks)
        self.chunkList = []
        self.chunkList.append([])
        self.chunkList[0].append(Chunk(self.app).chunk)

    def displayMap(self, app=None):
        if app:
            # Loop through Y levels in list
            for i in range(len(self.chunkList)):
                # Loop through X vals in list
                for k in range(len(self.chunkList[i][0])):
                    # Loop through One X val in list
                    Chunk = ""
                    for j in range(len(self.chunkList[i])):
                        # Loop through chars in list
                        for l in range(len(self.chunkList[i][j][k])):
                            if not isinstance(self.chunkList[i][j][k][l], str):
                                Chunk += str(self.chunkList[i][j][k][l].icon)+" "
                            else:
                                Chunk += str(self.chunkList[i][j][k][l])+" "
                    app.write(Chunk)
        else:
            # Loop through Y levels in list
            for i in range(len(self.chunkList)):
                # Loop through X vals in list
                for k in range(len(self.chunkList[i][0])):
                    # Loop through One X val in list
                    Chunk = ""
                    for j in range(len(self.chunkList[i])):
                        # Loop through chars in list

                        for l in range(len(self.chunkList[i][j][k])):
                            # If it's an obj, print the icon
                            if not isinstance(self.chunkList[i][j][k][l], str):
                                Chunk += str(self.chunkList[i]
                                             [j][k][l].icon)+" "
                            else:
                                Chunk += str(self.chunkList[i][j][k][l])+" "
                    print(Chunk)

    def newChunkX(self, yLevel):
        '''
        Create a new chunk on the
        map
        yLevel -> 1++
        '''
        # Add a new chunk on a certain y level
        self.chunkList[int(yLevel-1)].append(Chunk(self.app).chunk)

    def newChunkY(self):
        '''
        Create a new chunk on the
        map
        '''
        # Add a new chunk on the next Y level
        self.chunkList.append([])
        self.chunkList[-1].append(Chunk(self.app).chunk)


class Chunk:

    def __init__(self, app):
        '''
        Create a new chunk
        that will be mapped
        on the map

        size -> Grid Size
        default size is 5
        '''
        # with open("gameSettings.json", "r") as f:
        #settings = json.load(f)
        #size = settings["Settings"]["Chunk Size"]

        size = 5

        # Create chunk template
        chunk = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append("⚪")
            chunk.append(row)
        # Add randomly spawned world structures to template
        self.chunk = self.genWorldStructures(chunk, app)

    def genWorldStructures(self, chunk, app):
        # Was going to create a method to pull different types, decided against it
        structures = {"enemy", "town", "largeTown", "Dungeon", "Mountain"}
        for i in range(len(chunk)):
            for j in range(len(chunk[i])):
                if len(chunk) > 2:
                    # 1 in 4 chance to spawn a structure
                    if random.randint(0, len(chunk)-2) == len(chunk)-2:
                        structure = random.choice(list(structures))
                        if structure == "enemy":
                            structure = struc.Enemy(app)
                        elif structure == "town":
                            structure = struc.Town(app)
                        elif structure == "largeTown":
                            structure = struc.LargeTown(app)
                        elif structure == "Dungeon":
                            structure = struc.Dungeon(app)
                        elif structure == "Mountain":
                            structure = struc.Mountain(app)
                        chunk[i][j] = structure
        # Make sure there is at least 1 type of each structure in the chunk
        self.chunk = self.fixWorldStructures(chunk, structures, app)

        return chunk

    def fixWorldStructures(self, chunk, structures, app):
        '''
        Makes sure there is at least 1 of each type
        of building in the chunk!
        '''
        # Checks to make sure it's in there
        chunkChecks = [False, False, False, False, False]

        for y in range(len(chunk)):

            for x in range(len(chunk[y])):

                if chunk[y][x].__class__ == struc.Enemy(app).__class__:
                    chunkChecks[0] = True

                if chunk[y][x].__class__ == struc.Town(app).__class__:
                    chunkChecks[1] = True

                if chunk[y][x].__class__ == struc.LargeTown(app).__class__:
                    chunkChecks[2] = True

                if chunk[y][x].__class__ == struc.Dungeon(app).__class__:
                    chunkChecks[3] = True

                if chunk[y][x].__class__ == struc.Mountain(app).__class__:
                    chunkChecks[4] = True
        # Loop through and place the structure at a random open point if it isn't in the map already
        for i in range(len(chunk)):

            for j in range(len(chunk[i])):

                x = random.randrange(0, len(chunk))
                y = random.randrange(0, len(chunk))

                if not chunkChecks[0]:
                    if chunk[y][x] == '⚪':
                        chunk[y][x] = struc.Enemy(app)
                        # Getting issues using 'chunk = self.fixWorldStructures(chunk, structures, app)'
                        # But when I take it out it isn't doing what I want it to?
                        return self.fixWorldStructures(chunk, structures, app)

                elif not chunkChecks[1]:
                    if chunk[y][x] == '⚪':
                        chunk[y][x] = struc.Town(app)
                        return self.fixWorldStructures(chunk, structures, app)

                elif not chunkChecks[2]:
                    if chunk[y][x] == '⚪':
                        chunk[y][x] = struc.LargeTown(app)
                        return self.fixWorldStructures(chunk, structures, app)

                elif not chunkChecks[3]:
                    if chunk[y][x] == '⚪':
                        chunk[y][x] = struc.Dungeon(app)
                        return self.fixWorldStructures(chunk, structures, app)

                elif not chunkChecks[4]:
                    if chunk[y][x] == '⚪':
                        chunk[y][x] = struc.Mountain(app)
                        return self.fixWorldStructures(chunk, structures, app)

        if (chunkChecks[0] and chunkChecks[1] and chunkChecks[2] and chunkChecks[3] and chunkChecks[4]):
            # return the fixed chunk
            return chunk

if __name__ == "__main__":
    map = Map()
    map.newChunkX(1)
    map.newChunkY(1)
    map.displayMap()
