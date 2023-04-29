from typing import NamedTuple

name = 'ЦСК'
img = 'asdasdq213.img'
start = 12312  # posix format
end = 123123  # posix format
league = 'Чемпионат Англии. Премьер-лига'
book_name = '1xbet'
match_id = 1231
league_id = 12312
sport = 'football'
bets = 'bets object'
match_info = {
    'bookmaker_info': {
        'name': book_name,
        'match_id': match_id,
        'league_id': league_id
    },
    'league': league,
    'teams': {
        'tram_1':
            {
                'name': name,
                'img': img
            },
        'tram_2':
            {
                'name': name,
                'img': img
            }
    },
    'start': start,
    'sport': sport,
    'bets': bets
}

result = {
    'end': end,
    'teams_results': {
        'team_1': {
            'goals': 3,
            'parts_info': [1, 2]
        },
        'team_2': {
            'goals': 0,
            'parts_info': [0, 0]
        }

    }
}

print(match_info)


class Coordinate(NamedTuple):
    x: float
    y: float

def get_coordinate()->Coordinate:
    return Coordinate(1,2)
