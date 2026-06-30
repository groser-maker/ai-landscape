import { LightningElement, api, track } from 'lwc';
import { NavigationMixin as navigationMixin } from 'lightning/navigation';

const BUILDER_SUBTYPES = [
        { label: 'Deployment Strategist', value: 'Deployment Strategist' },
        { label: 'FDE', value: 'FDE' },
        { label: 'Graduate Builder', value: 'Graduate Builder' }
    ],
    GRID_SNAP = 10,
    MAX_TITLE_LEN = 28,
    NavBase = navigationMixin(LightningElement),
    ROLE_OPTIONS = [
        { label: 'People Manager', value: 'People Manager' },
        { label: 'Individual Contributor', value: 'Individual Contributor' },
        { label: 'Executive Assistant', value: 'Executive Assistant' },
        { label: 'FuturForce Intern', value: 'FuturForce Intern' },
        { label: 'Other', value: 'Other' }
    ],
    SOLUTIONS_SUBTYPES = [
        { label: 'Account SE', value: 'Account SE' },
        { label: 'BizCon', value: 'BizCon' },
        { label: 'BVS', value: 'BVS' },
        { label: 'Enterprise Architect', value: 'Enterprise Architect' },
        { label: 'Industry Advisor', value: 'Industry Advisor' },
        { label: 'Specialist', value: 'Specialist' },
        { label: 'Strategic SE', value: 'Strategic SE' },
        { label: 'Technical Architect', value: 'Technical Architect' }
    ],
    STATUS_DOT_MAP = {
        'Backfill': 'status-dot status-dot--backfill',
        'In-Seat': 'status-dot status-dot--inseat',
        'Net New': 'status-dot status-dot--netnew'
    },
    STATUS_OPTIONS = [
        { label: 'In-Seat', value: 'In-Seat' },
        { label: 'Backfill', value: 'Backfill' },
        { label: 'Net New', value: 'Net New' }
    ],
    TYPE_OPTIONS = [
        { label: 'Solutions', value: 'Solutions' },
        { label: 'Builder', value: 'Builder' }
    ],
    ZERO = 0,
    snapToGrid = function snapToGrid(value) { return Math.round(value / GRID_SNAP) * GRID_SNAP; };

export default class PersonCard extends NavBase {
    @api person;
    @track showPopover = false;
    @track editStatus = '';
    @track editRole = '';
    @track editType = '';
    @track editSubType = '';

    roleOptions = ROLE_OPTIONS;
    statusOptions = STATUS_OPTIONS;
    typeOptions = TYPE_OPTIONS;

    dragStartX = ZERO;
    dragStartY = ZERO;
    origX = ZERO;
    origY = ZERO;
    isDragging = false;

    get posX() { return this.person.PositionX__c || ZERO; }
    get posY() { return this.person.PositionY__c || ZERO; }

    get cardStyle() {
        return `transform: translate(${this.posX}px, ${this.posY}px);`;
    }

    get cardClass() {
        let base = 'person-card person-card--solutions';
        if (this.person.Type__c === 'Builder') {
            base = 'person-card person-card--builder';
        }
        if (this.isDragging) { return `${base} person-card--dragging`; }
        return base;
    }

    get typeDot() {
        if (this.person.Type__c === 'Builder') { return 'type-dot type-dot--builder'; }
        return 'type-dot type-dot--solutions';
    }

    get statusDotClass() {
        return STATUS_DOT_MAP[this.person.Status__c] || 'status-dot';
    }

    get shortTitle() {
        const title = this.person.Title__c || '';
        if (title.length > MAX_TITLE_LEN) { return `${title.substring(ZERO, MAX_TITLE_LEN)}…`; }
        return title;
    }

    get subTypeOptions() {
        if (this.editType === 'Builder') { return BUILDER_SUBTYPES; }
        return SOLUTIONS_SUBTYPES;
    }

    attachDragListeners(card, pointerId) {
        card.setPointerCapture(pointerId);
        card.addEventListener('pointermove', this.pointerMoveHandler);
        card.addEventListener('pointerup', this.pointerUpHandler);
    }

    handlePointerDown(event) {
        if (event.button !== ZERO) { return; }
        this.isDragging = false;
        this.dragStartX = event.clientX;
        this.dragStartY = event.clientY;
        this.origX = this.posX;
        this.origY = this.posY;
        this.attachDragListeners(this.template.querySelector('.person-card'), event.pointerId);
    }

    pointerMoveHandler = (event) => {
        const deltaX = event.clientX - this.dragStartX,
            deltaY = event.clientY - this.dragStartY;
        if (!this.isDragging && (Math.abs(deltaX) > GRID_SNAP || Math.abs(deltaY) > GRID_SNAP)) {
            this.isDragging = true;
        }
        if (this.isDragging) {
            this.dispatchEvent(new CustomEvent('cardmove', {
                bubbles: true,
                detail: {
                    id: this.person.Id,
                    posX: snapToGrid(this.origX + deltaX),
                    posY: snapToGrid(this.origY + deltaY)
                }
            }));
        }
    };

    pointerUpHandler = (event) => {
        const card = this.template.querySelector('.person-card');
        card.removeEventListener('pointermove', this.pointerMoveHandler);
        card.removeEventListener('pointerup', this.pointerUpHandler);
        if (this.isDragging) {
            this.dispatchEvent(new CustomEvent('carddrop', {
                bubbles: true,
                detail: {
                    id: this.person.Id,
                    posX: snapToGrid(this.origX + (event.clientX - this.dragStartX)),
                    posY: snapToGrid(this.origY + (event.clientY - this.dragStartY))
                }
            }));
        } else {
            this.openPopover();
        }
        this.isDragging = false;
    };

    handleKeyDown(event) {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            this.openPopover();
        }
    }

    openPopover() {
        this.editStatus = this.person.Status__c;
        this.editRole = this.person.Role__c;
        this.editType = this.person.Type__c;
        this.editSubType = this.person.SubType__c;
        this.showPopover = true;
    }

    closePopover() {
        this.showPopover = false;
    }

    navigateToRecord() {
        this[navigationMixin.Navigate]({
            attributes: {
                actionName: 'view',
                recordId: this.person.Id
            },
            type: 'standard__recordPage'
        });
    }

    handleStatusChange(event) { this.editStatus = event.detail.value; }
    handleRoleChange(event) { this.editRole = event.detail.value; }
    handleTypeChange(event) {
        this.editType = event.detail.value;
        this.editSubType = '';
    }
    handleSubTypeChange(event) { this.editSubType = event.detail.value; }

    handleSave() {
        this.dispatchEvent(new CustomEvent('personedit', {
            bubbles: true,
            detail: {
                id: this.person.Id,
                role: this.editRole,
                status: this.editStatus,
                subType: this.editSubType,
                type: this.editType
            }
        }));
        this.showPopover = false;
    }
}
