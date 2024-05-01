from repositories.tickets_set import TicketsSetFileRepository, TicketsSetRepository


class TicketsSetService:
    def __init__(
        self,
        ticket_set_file_repository: TicketsSetFileRepository,
        ticket_set_repository: TicketsSetRepository,
    ) -> None:
        self._ticket_set_file_repository = ticket_set_file_repository
        self._ticket_set_repository = ticket_set_repository
    
