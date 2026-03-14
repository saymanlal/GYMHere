/**
 * Member service - API calls for member management
 */
import { apiService, PaginatedResponse, ApiResponse } from "@/services/api";
import {
  Member,
  MemberListItem,
  CreateMemberData,
  UpdateMemberData,
  MemberStats,
  Lead,
  LeadListItem,
  CreateLeadData,
  LeadStats,
} from "../types";

class MemberService {
  /**
   * Get paginated list of members
   */
  async getMembers(params?: {
    page?: number;
    pageSize?: number;
    status?: string;
    search?: string;
  }): Promise<PaginatedResponse<MemberListItem>> {
    return apiService.get<PaginatedResponse<MemberListItem>>("/members/", params);
  }

  /**
   * Get single member by ID
   */
  async getMember(id: string): Promise<Member> {
    const response = await apiService.get<ApiResponse<Member>>(`/members/${id}/`);
    return response.data;
  }

  /**
   * Create new member
   */
  async createMember(data: CreateMemberData): Promise<Member> {
    const response = await apiService.post<ApiResponse<Member>>("/members/", data);
    return response.data;
  }

  /**
   * Update member
   */
  async updateMember(id: string, data: UpdateMemberData): Promise<Member> {
    const response = await apiService.patch<ApiResponse<Member>>(`/members/${id}/`, data);
    return response.data;
  }

  /**
   * Delete member
   */
  async deleteMember(id: string): Promise<void> {
    await apiService.delete(`/members/${id}/`);
  }

  /**
   * Activate member
   */
  async activateMember(id: string): Promise<Member> {
    const response = await apiService.post<ApiResponse<Member>>(`/members/${id}/activate/`);
    return response.data;
  }

  /**
   * Deactivate member
   */
  async deactivateMember(id: string): Promise<Member> {
    const response = await apiService.post<ApiResponse<Member>>(`/members/${id}/deactivate/`);
    return response.data;
  }

  /**
   * Suspend member
   */
  async suspendMember(id: string): Promise<Member> {
    const response = await apiService.post<ApiResponse<Member>>(`/members/${id}/suspend/`);
    return response.data;
  }

  /**
   * Get member statistics
   */
  async getMemberStats(): Promise<MemberStats> {
    const response = await apiService.get<ApiResponse<MemberStats>>("/members/stats/");
    return response.data;
  }

  /**
   * Search members
   */
  async searchMembers(query: string): Promise<MemberListItem[]> {
    const response = await apiService.get<ApiResponse<MemberListItem[]>>("/members/search/", {
      q: query,
    });
    return response.data;
  }

  // Lead Management

  /**
   * Get paginated list of leads
   */
  async getLeads(params?: {
    page?: number;
    pageSize?: number;
    status?: string;
    search?: string;
  }): Promise<PaginatedResponse<LeadListItem>> {
    return apiService.get<PaginatedResponse<LeadListItem>>("/members/leads/", params);
  }

  /**
   * Get single lead by ID
   */
  async getLead(id: string): Promise<Lead> {
    const response = await apiService.get<ApiResponse<Lead>>(`/members/leads/${id}/`);
    return response.data;
  }

  /**
   * Create new lead
   */
  async createLead(data: CreateLeadData): Promise<Lead> {
    const response = await apiService.post<ApiResponse<Lead>>("/members/leads/", data);
    return response.data;
  }

  /**
   * Update lead
   */
  async updateLead(id: string, data: Partial<CreateLeadData>): Promise<Lead> {
    const response = await apiService.patch<ApiResponse<Lead>>(`/members/leads/${id}/`, data);
    return response.data;
  }

  /**
   * Delete lead
   */
  async deleteLead(id: string): Promise<void> {
    await apiService.delete(`/members/leads/${id}/`);
  }

  /**
   * Convert lead to member
   */
  async convertLead(id: string, memberData: CreateMemberData): Promise<Member> {
    const response = await apiService.post<ApiResponse<Member>>(
      `/members/leads/${id}/convert/`,
      { member_data: memberData }
    );
    return response.data;
  }

  /**
   * Get lead statistics
   */
  async getLeadStats(): Promise<LeadStats> {
    const response = await apiService.get<ApiResponse<LeadStats>>("/members/leads/stats/");
    return response.data;
  }
}

export const memberService = new MemberService();